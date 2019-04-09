import json
from pprint import pprint
from elasticsearch import Elasticsearch
es = Elasticsearch()
import regex
from elasticsearch.helpers import bulk, streaming_bulk
from datetime import datetime
from datetime import timedelta
import os
from pygrok import Grok
import time
import traceback
import logging
import copy
import sys
import time

def gendata(list):

    for data in list:
        yield data


def bulk_data_to_elastic(data, index_name):

    for ok, result in streaming_bulk(
            es,
            gendata(data),
            index=index_name,
            doc_type=index_name,
            chunk_size=250  # keep the batch sizes small for appearances only
            ):
        action, result = result.popitem()
        doc_id = '/%s/doc/%s' % (index_name, result['_id'])
        # process the information from ES whether the document has been
        # successfully indexed
        if not ok:
            print('Failed to %s document %s: %r' % (action, doc_id, result))
        else:
            print(doc_id)

def create_indice_if_not_exists(file_name_with_extention):

    filename = os.path.splitext(file_name_with_extention)[0].lower()
    if not es.indices.exists(index=filename):
        clone_mapping_indice = copy.deepcopy(mapping_indice)
        mapping_index = clone_mapping_indice['mappings']['test']
        clone_mapping_indice['mappings'][filename] = mapping_index
        del clone_mapping_indice['mappings']['test']
        es.indices.create(index=filename, body=clone_mapping_indice)




def error_extractor(log_file):

    error_line = log_file.readline()
    string_error = ''
    if error_line.rstrip('\r\n') == ERROR_START_END_PATTERN:
        error_line = log_file.readline()
        while(error_line and error_line.rstrip('\r\n') != ERROR_START_END_PATTERN ):
            string_error = string_error + ' ' + error_line.rstrip('\r\n')
            error_line = log_file.readline()


    return string_error


def error_audit_extractor(log_file):
    error_object = {}
    code_error = log_file.readline()
    if not code_error:
        return None
    tab_code = code_error.split(':')
    if tab_code.__len__() >0:
        error_object['code'] = tab_code[1].replace('"','').replace(',','').rstrip('\r\n')

    message_error = log_file.readline()

    if not message_error:
        return error_object

    tab_code_m = message_error.split(':')
    if tab_code_m.__len__() >0:
        error_object['message'] = tab_code_m[1].replace('"','').rstrip('\r\n')
    log_file.readline()

    return error_object

def extract_main_log_information(json_log_line, log_file):
    # extract execution time
    log_execution_time_pattern = 'took %{NUMBER:execution_time}ms'
    grok_execution_time_pattern = Grok(log_execution_time_pattern)
    execution_time = grok_execution_time_pattern.match(json_log_line.get('log'))
    json_log_line["execution_time"] = execution_time.get('execution_time') if execution_time else None

    # extract url
    log_url_pattern = 'Http call to : %{SOS_URL_PATTERN:url_host}'
    grok_url_pattern = Grok(log_url_pattern, custom_regex_folder)
    url_host = grok_url_pattern.match(json_log_line.get('log'))
    if url_host:
        json_log_line["url_host"] = url_host.get('url_host')
        json_log_line["type_log"] = "HTTP_CALL"

    # extract Dataweave
    log_dataweave = 'Dataweave processing time %{NOTSPACE:dataweave}'
    grok_dataweave = Grok(log_dataweave)
    dataweave = grok_dataweave.match(json_log_line.get('log'))
    if dataweave:
        json_log_line["dataweave"] = dataweave.get('dataweave')
        json_log_line["type_log"] = "dataweave"

    # extract Subflow
    log_subflow = 'Subflow processing time %{NOTSPACE:subflow}'
    grok_subflow = Grok(log_subflow)
    subflow = grok_subflow.match(json_log_line.get('log'))
    if subflow:
        json_log_line["subflow"] = subflow.get('subflow')
        json_log_line["type_log"] = "subflow"

    # extract ScriptTransformer
    log_scriptTransformer = 'ScriptTransformer processing time ScriptTransformer%{SOS_JSON_WITH_EQUAL:scriptTransformer}'
    grok_scriptTransformer = Grok(log_scriptTransformer, custom_regex_folder)
    scriptTransformer = grok_scriptTransformer.match(json_log_line.get('log'))
    if scriptTransformer:
        json_log_line["scriptTransformer"] = scriptTransformer.get('scriptTransformer')
        json_log_line["type_log"] = "scriptTransformer"

    # extract BuildingSummaryFlow
    log_buildingSummaryFlow = 'to process event \[%{NOTSPACE:buildingSummaryFlow}\]'
    grok_buildingSummaryFlow = Grok(log_buildingSummaryFlow)
    buildingSummaryFlow = grok_buildingSummaryFlow.match(json_log_line.get('log'))
    if buildingSummaryFlow:
        json_log_line["buildingSummaryFlow"] = buildingSummaryFlow.get('buildingSummaryFlow')
        json_log_line["type_log"] = "buildingSummaryFlow"


    # extract error audit
    if (json_log_line.get('loglevel') == "ERROR" and json_log_line.get('log') =='ERROR AUDIT  - {'):
        error_audit = error_audit_extractor(log_file)
        if (error_audit):
            json_log_line['error_code'] = error_audit.get('code')
            json_log_line['error_message'] = error_audit.get('message')

    elif (json_log_line.get('loglevel') == "ERROR"):
        error_classic = error_extractor(log_file)

        message_error_pattern = 'Message               : %{GREEDYDATA:message} Element'
        grok_message_error_pattern = Grok(message_error_pattern)
        message_error_pattern = grok_message_error_pattern.match(error_classic)
        if message_error_pattern:
            json_log_line["error_message"] = message_error_pattern.get('message')

        element_error_pattern = 'Element               : %{GREEDYDATA:element} -'
        grok_element_error_pattern = Grok(element_error_pattern)
        element_error_pattern = grok_element_error_pattern.match(error_classic)
        if element_error_pattern:
            json_log_line["error_element"] = element_error_pattern.get('element')

        stack_error_pattern = 'Exception stack is:%{GREEDYDATA:stack}'
        grok_stack_error_pattern = Grok(stack_error_pattern)
        stack_error_pattern = grok_stack_error_pattern.match(error_classic)
        if stack_error_pattern:
            json_log_line["error_stack"] = stack_error_pattern.get('stack')


    return json_log_line


def proc_filtered_log(file_path):
    pattern = '\[%{TIMESTAMP_ISO8601:timestamp}\] %{LOGLEVEL:loglevel}%{SOS_SPACE}%{NOTSPACE:package} \[%{NOTSPACE:config}\]: %{GREEDYDATA:log}'
    listobject = []
    number_line = 0
    with open(file_path, encoding="utf8") as log_file:
        grok = Grok(pattern, custom_regex_folder)
        # Grok(pattern,None, {'WHOLE_LINE':'.*|$'})
        log_text = log_file.readline()
        start = time.time()
        while log_text:
            json_log_line = grok.match(log_text)
            if json_log_line:
                json_log_line = extract_main_log_information(json_log_line, log_file)
                listobject.append(json_log_line)
            try:
                log_text = log_file.readline()
            except Exception as erro:
                exception = traceback.format_exc()
                logging.error(exception)

    return listobject



def log_file_to_json(file_path, file_name_with_extention):
    file_name = os.path.splitext(file_name_with_extention)[0]
    #if file_name_with_extention.startswith("exp-filtered.log"):
    list_file_logs[file_name] = proc_filtered_log(file_path)
        #pprint(list_file_logs)

current_directory = os.getcwd()
log_directory = "logs"
current_milli_time = lambda: int(round(time.time() * 1000))
path_files_folder = os.path.join(current_directory, log_directory)
if len(sys.argv) > 1:
    path_files_folder = sys.argv[1]


custom_regex_folder = os.path.join(current_directory, 'custom_regex_folder')
list_file_logs = {}
ERROR_START_END_PATTERN = '********************************************************************************'
mapping_indice = {"settings":{"number_of_shards":1,"number_of_replicas":1},"mappings":{"test":{"properties":{"buildingSummaryFlow":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"config":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"dataweave":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"error_element":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"error_message":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"error_stack":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"execution_time":{"type":"integer"},"log":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"loglevel":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"package":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"scriptTransformer":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"subflow":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"timestamp":{"type":"date","format":"yyyy-MM-dd HH:mm:ss.SSS"},"type_log":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"url_host":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}}}}}}
# r=root, d=directories, f = files
for r, d, f in os.walk(path_files_folder):
    for file in f:
        if file.endswith('.log'):
            print(os.path.join(r, file))
            create_indice_if_not_exists(file)
            log_file_to_json(os.path.join(r, file), file)



for index_key in list_file_logs:
    index = list_file_logs[index_key]
    bulk_data_to_elastic(index, index_key.lower())


for r, d, f in os.walk(path_files_folder):
    for file in f:
        if file.endswith('.log'):
            complete_file_path = os.path.join(r, file)
            renamed_complete_file_path = complete_file_path + '.' + str(current_milli_time()) + '.archive'
            os.rename(complete_file_path, renamed_complete_file_path)
            print('%s has been renamed to %s' %(complete_file_path, renamed_complete_file_path))






