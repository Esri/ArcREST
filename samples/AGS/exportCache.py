# coding=utf-8
"""
Demonstrates the usage of GPServer and GPTask and GPJobs
"""
from time import sleep

import arcrest


def get_parameter(params, param_name):
    for param in params:
        if param['name'] == param_name:
            return param

    return None


def print_message(message):
    if ('type' in message) and ('description' in message):
        print("{}: {}".format(message['type'], message['description']))
    else:
        print(message)


if __name__ == '__main__':
    username = "siteadmin"
    password = "geo2014!"

    ags_url = "http://192.168.20.21:6080/arcgis"
    map_service = "ImageBaseMap:Mapserver"

    # get service information
    service = arcrest.ags.server.MapService(
            "{}/rest/services/{}".format(ags_url, map_service.replace(":", "/")))

    # check if the service is cached
    print(service.singleFusedMapCache)
    if not service.singleFusedMapCache:
        print("Service has no cache")
        exit(-1)

    # retrieve scales from the service
    print(service.tileInfo)
    lods = service.tileInfo["lods"]
    print(lods)

    lod2scale = {}
    for lod in lods:
        level = int(lod['level'])
        scale = lod['scale']
        lod2scale[level] = "{:.6f}".format(scale)
    print(lod2scale)

    # create a security handler
    sh = arcrest.AGSTokenSecurityHandler(
        username=username,
        password=password,
        token_url=ags_url + "/tokens/",
        org_url=ags_url)

    gp_export_url = "{}/rest/services/System/CachingTools/GPServer".format(ags_url)
    gp_service = arcrest.ags.server.GPService(gp_export_url, sh)

    # show all tasks
    print(gp_service.tasks)

    # get the cache export task
    export_cache_task = None
    for task in gp_service.tasks:
        if task.name == "ExportCache":
            export_cache_task = task
            break

    if export_cache_task:
        # get the parameter
        params = export_cache_task.parameters
        params1 = export_cache_task.parameters

        p_service_url = get_parameter(params, "service_url")
        p_target_cache = get_parameter(params, "target_cache")
        p_storage_format = get_parameter(params, "storage_format_type")
        p_copy_data_from_server = get_parameter(params, "copy_data_from_server")
        p_tile_package = get_parameter(params, "tile_package")
        p_levels = get_parameter(params, "levels")
        p_replace_existing_tiles = get_parameter(params, "replace_existing_tiles")
        p_thread_count = get_parameter(params, "thread_count")
        p_area_of_interest = get_parameter(params, "area_of_interest")
        p_out_service_url = get_parameter(params, "out_service_url")
        p_export_options = get_parameter(params, "export_options")
        p_temp_output_path = get_parameter(params, "temp_output_path")
        p_export_extent = get_parameter(params, "export_extent")

        # set service parameter
        service_url = p_service_url['defaultValue']
        service_url.value = map_service

        target_cache = p_target_cache['defaultValue']
        target_cache.value = "D:\exp_cache"

        storage_format = p_storage_format['defaultValue']
        storage_format.value = "COMPACT"

        copy_data_from_server = p_copy_data_from_server['defaultValue']
        copy_data_from_server.value = False

        tile_package = p_tile_package['defaultValue']
        tile_package.value = False

        levels = p_levels['defaultValue']
        levels.value = lod2scale[0] + ";" + lod2scale[1]

        thread_count = p_thread_count['defaultValue']
        thread_count.value = 1

        replace_existing_tiles = p_replace_existing_tiles['defaultValue']
        replace_existing_tiles.value = True

        # create the job
        job = export_cache_task.submitJob([service_url, target_cache,
                                           storage_format, copy_data_from_server, tile_package,
                                           levels, thread_count, replace_existing_tiles])

        # wait until the job finishes
        last_message_index = 0
        while job.jobStatus in ["esriJobSubmitted", "esriJobExecuting", "esriJobWaiting"]:
            print("Job status: {}".format(job.jobStatus))
            messages = job.messages
            while last_message_index < len(messages):
                print_message(messages[last_message_index])

                last_message_index += 1

            sleep(5)

        # print the final messages
        print("Job status: {}".format(job.jobStatus))
        messages = job.messages
        for i in range(last_message_index, len(messages)):
            print_message(messages[i])
