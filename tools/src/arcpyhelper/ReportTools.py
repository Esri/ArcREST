import datetime
import os
import arcpyhelper.Common as Common
import arcpy
from arcpy import env
from copy import deepcopy
import gc
import time

from dateutil.parser import parse

dateTimeFormat = '%Y-%m-%d %H:%M'

class ReportToolsError(Exception):
    """ raised when error occurs in utility module functions """
    pass
#----------------------------------------------------------------------
def create_report_layers_using_config(config):


    reporting_areas_ID_field = None
    reporting_areas = None
    reports = None      
    report_msg = None      
    try:
        
        reports =  config['Reports']
     
        report_msg = []        
        for i in reports:
            if i['Type'].upper()== "JOINCALCANDLOAD":
                create_calcload_report(report_params=i)                                   
            elif i['Type'].upper()== "RECLASS":
                reporting_areas = i ['ReportingAreas']
                if not os.path.isabs(reporting_areas):
                    reporting_areas = os.path.abspath(reporting_areas)
        
        
                reporting_areas_ID_field = i ['ReportingAreasIDField']

                report_msg.append(create_reclass_report(reporting_areas=reporting_areas,
                                     reporting_areas_ID_field=reporting_areas_ID_field,
                                     report_params=i))
            elif i['Type'].upper()== "AVERAGE":
                reporting_areas = i['ReportingAreas']
                if not os.path.isabs(reporting_areas):
                    reporting_areas =os.path.abspath(reporting_areas)
                
                reporting_areas_ID_field = i['ReportingAreasIDField']
                
                report_msg.append(create_average_report(reporting_areas=reporting_areas,
                                     reporting_areas_ID_field=reporting_areas_ID_field,
                                     report_params=i))
            else:
                print "Unsupported report type"
        if 'error' in report_msg:
            return False
        else:
            return True
 

    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "create_report_layers_using_config",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "create_report_layers_using_config",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    
    finally:
        reports = None        
        report_msg = None
        reporting_areas_ID_field = None
        reporting_areas = None   
        del reports
        del report_msg 
        del reporting_areas_ID_field 
        del reporting_areas   
        
        gc.collect()
#----------------------------------------------------------------------
def create_calcload_report(report_params):

    filt_layer = None
    reporting_layer = None 
    reporting_layer_id_field = None
    joinInfo = None
    field_map = None
    sql = None
    report_date = None
    report_schema = None
    report_result = None
    _tempWorkspace = None
    _tempTableName = None
    _tempTableFull = None  
    _procData = None
    inputCnt = None
    try:
      
        filt_layer = "filter_layer"

        reporting_layer = report_params['Data']
        reporting_layer_id_field = report_params['DataIDField']
        joinInfo = report_params['JoinInfo']
        
        field_map = report_params['FieldMap']

        sql = report_params['FilterSQL']

        report_date = report_params["ReportDateField"]
        report_schema = report_params['ReportResultSchema']
        report_result = report_params['ReportResult']

        #if not os.path.isabs(report_result):
            #report_result = os.path.abspath( report_result)

        #if not os.path.isabs(report_schema):
            #report_schema = os.path.abspath( report_schema)
            
        _tempWorkspace = env.scratchGDB    
        _tempTableName = Common.random_string_generator()
        _tempTableFull = os.path.join(_tempWorkspace, _tempTableName)
        
        
        if sql == '' or sql is None or sql == '1=1' or sql == '1==1':
            filt_layer = reporting_layer
        else:
            #arcpy.MakeQueryTable_management(in_table=reporting_layer,out_table=filt_layer,in_key_field_option="USE_KEY_FIELDS",in_key_field="#",in_field="#",where_clause=sql)
            try:            
                arcpy.MakeFeatureLayer_management(reporting_layer, filt_layer, sql, "", "")
                
            except:      
                try:                
                    arcpy.TableToTable_conversion(in_rows=reporting_layer,out_path=_tempWorkspace,out_name=_tempTableName)
                                                      
                    arcpy.MakeTableView_management(in_table=_tempTableFull, out_view= filt_layer, where_clause=sql,workspace="#",field_info="#")                
                 
                except:      
                    pass
        inputCnt = int(arcpy.GetCount_management(in_rows=filt_layer)[0])
        arcpy.Copy_management(report_schema,report_result,"FeatureClass")
                      
        if inputCnt == 0:
            
            print "            %s was created" % report_result
        else:

            _procData = calculate_load_results(feature_data = joinInfo['FeatureData'], 
                             feature_data_id_field = joinInfo['FeatureDataIDField'],                          
                            join_table = filt_layer, 
                            join_table_id_field = reporting_layer_id_field,
                            report_date_field=report_date,
                            report_result = report_result, 
                            field_map = field_map
                            )
            
            
            
            deleteFC([_procData])
            if arcpy.Exists(_tempTableFull):
                deleteFC([_tempTableFull])

            print "            %s was created" % report_result

    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "create_calcload_report",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "create_calcload_report",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        filt_layer = None
        reporting_layer = None 
        reporting_layer_id_field = None
        joinInfo = None
        field_map = None
        sql = None
        report_date = None
        report_schema = None
        report_result = None
        _tempWorkspace = None
        _tempTableName = None
        _tempTableFull = None  
        _procData = None
        inputCnt = None        
        
        del filt_layer
        del reporting_layer 
        del reporting_layer_id_field
        del joinInfo 
        del field_map 
        del sql 
        del report_date 
        del report_schema 
        del report_result 
        del _tempWorkspace 
        del _tempTableName 
        del _tempTableFull 
        del _procData
        del  inputCnt  
        
        gc.collect()
#----------------------------------------------------------------------
def create_reclass_report(reporting_areas,reporting_areas_ID_field,report_params):
    classified_layer_field_name = None
    filt_layer = None
    reporting_layer = None
    field_map = None
    sql = None
    count_field = None
    reclass_map = None
    report_schema = None
    report_result = None    
    report_date_field = None
    report_ID_field = None
    result_exp = None
    inputCnt = None
    classified_layer = None
    pivot_layer = None
    report_copy = None  
    try:

        classified_layer_field_name = "reclass"

        filt_layer = "filter_layer"

        reporting_layer = report_params['Data']
        field_map = report_params['FieldMap']
        sql = report_params['FilterSQL']


        count_field = report_params['CountField']
        reclass_map = report_params['ReclassMap']

        report_schema = report_params['ReportResultSchema']
        report_result = report_params['ReportResult']
        
        if not os.path.isabs(report_result):
            report_result =os.path.abspath( report_result)

        if not os.path.isabs(report_schema):
            report_schema =os.path.abspath( report_schema)

        report_date_field = report_params['ReportDateField']
        report_ID_field = report_params['ReportIDField']
        result_exp = report_params['FinalResultExpression']

        #if type(value_field) is tuple:
        #    average_value = value_field[1]
        #    value_field = value_field[0]

        if sql == '' or sql is None or sql == '1=1' or sql == '1==1':
            filt_layer = reporting_layer
        else:
            #arcpy.MakeQueryTable_management(in_table=reporting_layer,out_table=filt_layer,in_key_field_option="USE_KEY_FIELDS",in_key_field="#",in_field="#",where_clause=sql)
            arcpy.MakeFeatureLayer_management(reporting_layer, filt_layer, sql, "", "")

        inputCnt = int(arcpy.GetCount_management(in_rows=filt_layer)[0])
        if inputCnt == 0:
            copy_empty_report(reporting_areas=reporting_areas, reporting_areas_ID_field=reporting_areas_ID_field,
                              report_schema=report_schema,
                              report_result=report_result,
                              reclass_map=reclass_map,
                              report_date_field=report_date_field,
                              report_ID_field=report_ID_field)
            print "            %s was created" % report_result
        else:
            classified_layer = split_reclass(reporting_areas=reporting_areas, reporting_areas_ID_field=reporting_areas_ID_field,reporting_layer=filt_layer,field_map=field_map,
                                             reclass_map=reclass_map,classified_layer_field_name = classified_layer_field_name)

            pivot_layer = classified_pivot(classified_layer =classified_layer, classified_layer_field_name= classified_layer_field_name,
                                           reporting_areas_ID_field=reporting_areas_ID_field,count_field=count_field)

            report_copy = copy_report_data_schema(reporting_areas=reporting_areas,reporting_areas_ID_field=reporting_areas_ID_field,report_schema=report_schema,
                                                  report_result=report_result,join_layer=pivot_layer)


            calculate_report_results(report_result=report_result,  reporting_areas_ID_field=reporting_areas_ID_field,report_copy=report_copy,
                                     reclass_map=reclass_map, report_date_field=report_date_field,report_ID_field=report_ID_field, exp=result_exp)

            deleteFC([classified_layer,pivot_layer,report_copy])

            print "            %s was created" % report_result

    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "create_reclass_report",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "create_reclass_report",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        classified_layer_field_name = None
        filt_layer = None
        reporting_layer = None
        field_map = None
        sql = None
        count_field = None
        reclass_map = None
        report_schema = None
        report_result = None    
        report_date_field = None
        report_ID_field = None
        result_exp = None
        inputCnt = None
        classified_layer = None
        pivot_layer = None
        report_copy = None          
        
        del classified_layer_field_name 
        del filt_layer 
        del reporting_layer 
        del field_map 
        del sql 
        del count_field 
        del reclass_map 
        del report_schema 
        del report_result     
        del report_date_field 
        del report_ID_field 
        del result_exp 
        del inputCnt 
        del classified_layer 
        del pivot_layer 
        del report_copy   
        gc.collect()
        
#----------------------------------------------------------------------
def create_average_report(reporting_areas,reporting_areas_ID_field,report_params):
    filt_layer = None
    reporting_layer = None
    field_map = None
    sql = None
    code_exp = None
    report_schema = None
    report_result = None
    report_date_field = None
    report_ID_field = None
    avg_field_map = None
    inputCnt  = None
    result  = None
    report_copy  = None
   
    
    try:

        filt_layer = "filter_layer"
        reporting_layer = report_params['Data']
        field_map = report_params['FieldMap']
        sql = report_params['FilterSQL']

        code_exp = report_params['PreCalcExpression']

        report_schema = report_params['ReportResultSchema']
        report_result = report_params['ReportResult']

        if not os.path.isabs(report_result):
            report_result =os.path.abspath( report_result)

        if not os.path.isabs(report_schema):
            report_schema =os.path.abspath( report_schema)

        report_date_field = report_params['ReportDateField']
        report_ID_field = report_params['ReportIDField']

        avg_field_map = report_params['AverageToResultFieldMap']

        if sql == '' or sql is None or sql == '1=1' or sql == '1==1':
            filt_layer = reporting_layer
        else:
                      #arcpy.MakeQueryTable_management(in_table=reporting_layer,out_table=filt_layer,in_key_field_option="USE_KEY_FIELDS",in_key_field="#",in_field="#",where_clause=sql)
            arcpy.MakeFeatureLayer_management(reporting_layer, filt_layer, sql, "", "")

        inputCnt = int(arcpy.GetCount_management(in_rows=filt_layer).getOutput(0))
        if inputCnt == 0:
            pass
        else:

            result = split_average(reporting_areas=reporting_areas, reporting_areas_ID_field=reporting_areas_ID_field,reporting_layer=filt_layer,
                         reporting_layer_field_map=field_map,code_exp=code_exp)

            if 'layer' in result:

                report_copy = copy_report_data_schema(reporting_areas=reporting_areas,reporting_areas_ID_field=reporting_areas_ID_field,report_schema=report_schema,
                                                      report_result=report_result,join_layer=result['layer'])

                report_result = calculate_average_report_results(report_result=report_result,
                                                reporting_areas_ID_field=reporting_areas_ID_field ,
                                                report_copy=report_copy,
                                                field_map=avg_field_map,
                                                report_date_field=report_date_field,
                                                report_ID_field=report_ID_field,
                                                average_field=result['field'])
                print "            %s was created" % report_result



    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "create_average_report",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "create_average_report",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        filt_layer = None
        reporting_layer = None
        field_map = None
        sql = None
        code_exp = None
        report_schema = None
        report_result = None
        report_date_field = None
        report_ID_field = None
        avg_field_map = None
        inputCnt  = None
        result  = None
        report_copy  = None
        report_result  = None   
        
        del filt_layer
        del reporting_layer
        del field_map
        del sql
        del code_exp
        del report_schema
        del report_result
        del report_date_field 
        del report_ID_field
        del avg_field_map
        del inputCnt 
        del result 
        del report_copy 
              
        gc.collect()
#----------------------------------------------------------------------
def calculate_load_results(feature_data, 
                           feature_data_id_field,                         
                           join_table, 
                           join_table_id_field,
                           report_date_field,
                           report_result, 
                           field_map
                           ):
    
    _tempWorkspace = None     
    _feature_data_layer = None
    _join_table_copy = None
    _joinedDataFull = None   
    _pointsJoinedData = None
    _pointsJoinedDataFull = None  
    joinTableDesc = None
    joinName = None               
    featureDataDesc = None
    featureDataName = None    
    fields = None
    tFields = None 
    layerFlds  = None
    new_row = None
    dt = None
    onlTm = None
    timeStr = None
    strOnlineTime = None
    try:
        _tempWorkspace = env.scratchGDB
        
        _feature_data_layer = Common.random_string_generator()
        _join_table_copy = Common.random_string_generator()
        _joinedDataFull = os.path.join(_tempWorkspace, _join_table_copy)
        
        _pointsJoinedData = Common.random_string_generator()
        _pointsJoinedDataFull = os.path.join(_tempWorkspace, _pointsJoinedData)
        # Process: Make Feature Layer
        if arcpy.Exists(dataset = feature_data) == False:
            return {"Error": feature_data + " Does not exist"}
        
        if arcpy.Exists(dataset = join_table) == False:
            return {"Error": join_table + " Does not exist"}    
        
        arcpy.MakeFeatureLayer_management(in_features=feature_data, out_layer=_feature_data_layer, where_clause=None, workspace=None, field_info=None)
        
        # Process: Table to Table
        arcpy.TableToTable_conversion(join_table, _tempWorkspace, _join_table_copy, "", "#", "")
          
        # Process: Add Join
        arcpy.AddJoin_management(_feature_data_layer, feature_data_id_field, _joinedDataFull, join_table_id_field, "KEEP_COMMON")
        
        arcpy.FeatureClassToFeatureClass_conversion(_feature_data_layer, _tempWorkspace, _pointsJoinedData, "", "", "")
    
        joinTableDesc = arcpy.Describe(_joinedDataFull)
        joinName = str(joinTableDesc.name)    
                
        featureDataDesc = arcpy.Describe(feature_data)
        featureDataName = str(featureDataDesc.name)    
    
        try:    
            arcpy.RemoveJoin_management(_feature_data_layer, joinName)
        except:
            pass
        
        
        fields = []
        tFields = []       
        layerFlds = fieldsToFieldArray(featureclass = _pointsJoinedDataFull)
        
        for fld in field_map:
            if fld['FieldName'] in layerFlds:
            
             
                fields.append(fld['FieldName'])            
            elif joinName + "_" + fld['FieldName'] in layerFlds:
                fld['FieldName'] = joinName + "_" + fld['FieldName']
                fields.append( fld['FieldName'])
            elif featureDataName + "_" + fld['FieldName'] in layerFlds:
                fld['FieldName'] = featureDataName + "_" + fld['FieldName']
                fields.append( fld['FieldName'])                
            
        if len(fields) != len(field_map):    
            print "Field Map length does not match fields in layer, exiting"
            return
        
        for fld in field_map:
            tFields.append(fld['TargetField'])        
        
        
        tFields.append("SHAPE@")
        
        fields.append("SHAPE@")
        
        datefld = -1
        if report_date_field in tFields:
            datefld = tFields.index(report_date_field)
        elif report_date_field != '':
            tFields.append(report_date_field)
            
        with arcpy.da.InsertCursor(report_result,tFields) as icursor:
            strOnlineTime = Common.online_time_to_string(Common.local_time_to_online(),dateTimeFormat)
                                                          
            with arcpy.da.SearchCursor(_pointsJoinedDataFull, fields) as scursor:
                for row in scursor:
                    new_row=list(row)
                    if datefld > -1 :
                        dt = parse(new_row[datefld])
                        onlTm = Common.local_time_to_online(dt)
                        timeStr = Common.online_time_to_string(onlTm,dateTimeFormat)
                        new_row[datefld] = timeStr
                    elif report_date_field != '':    
                        new_row.append(strOnlineTime)  
                    icursor.insertRow(new_row)  
                del row
                del scursor
            del icursor
                    
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "calculate_load_results",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "calculate_load_results",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:            
        _tempWorkspace = None     
        _feature_data_layer = None
        _join_table_copy = None
        _joinedDataFull = None   
        _pointsJoinedData = None
        _pointsJoinedDataFull = None  
        joinTableDesc = None
        joinName = None               
        featureDataDesc = None
        featureDataName = None    
        fields = None
        tFields = None 
        layerFlds  = None
        new_row = None
        dt = None
        onlTm = None
        timeStr = None
        strOnlineTime = None 

        del _tempWorkspace    
        del _feature_data_layer
        del _join_table_copy
        del _joinedDataFull  
        del  _pointsJoinedData
        del _pointsJoinedDataFull  
        del joinTableDesc
        del joinName               
        del featureDataDesc
        del featureDataName    
        del fields
        del tFields 
        del layerFlds 
        del new_row
        del dt
        del onlTm
        del timeStr
        del strOnlineTime
        gc.collect()
#----------------------------------------------------------------------
def split_average(reporting_areas, reporting_areas_ID_field,reporting_layer, reporting_layer_field_map,code_exp):
    _tempWorkspace = None
    _intersect  = None
    sumstats = None
    age_field = None
    try:   
        _tempWorkspace = env.scratchGDB
    
        _intersect = os.path.join(_tempWorkspace ,Common.random_string_generator())
        sumstats = os.path.join(_tempWorkspace ,Common.random_string_generator())
    
        # Process: Intersect Reporting Areas with Reporting Data to split them for accurate measurements
        arcpy.Intersect_analysis(in_features="'"+ reporting_areas + "' #;'" + reporting_layer+ "' #",out_feature_class= _intersect,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")
    
        age_field="statsfield"
        # Process: Add a field and calculate it with the groupings required for reporting.  If CP is set, _CP will be apped to the end of the material type.
        arcpy.AddField_management(in_table=_intersect, field_name=age_field, field_type="LONG",field_precision= "", field_scale="", field_length="",
                                  field_alias="",field_is_nullable= "NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
    
        calc_field(inputDataset=_intersect,field_map=reporting_layer_field_map,code_exp=code_exp,result_field=age_field)
    
        arcpy.Statistics_analysis(_intersect,out_table=sumstats,statistics_fields=age_field + " MEAN",case_field=reporting_areas_ID_field)
    
        deleteFC([_intersect])
        return {"layer":sumstats,"field":"MEAN_"+age_field}
    
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "split_average",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "split_average",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:                
        _tempWorkspace = None
        _intersect  = None
       
        del _tempWorkspace
        del _intersect
        
        gc.collect()

#----------------------------------------------------------------------
def split_reclass(reporting_areas, reporting_areas_ID_field,reporting_layer, field_map,reclass_map,classified_layer_field_name):
   
    _tempWorkspace = None
    _intersect = None
    flds = None
    val_fnd = None
    sql_state = None
    newRow = None
    newRows = None
    
    try:
        _tempWorkspace = env.scratchGDB

        _intersect = os.path.join(_tempWorkspace ,Common.random_string_generator())
    
        # Process: Intersect Reporting Areas with Reporting Data to split them for accurate measurements
        arcpy.Intersect_analysis(in_features="'"+ reporting_areas + "' #;'" + reporting_layer+ "' #",out_feature_class= _intersect,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")
    
        # Process: Add a field and calculate it with the groupings required for reporting.  If CP is set, _CP will be apped to the end of the material type.
        arcpy.AddField_management(in_table=_intersect, field_name=classified_layer_field_name, field_type="TEXT",field_precision= "", field_scale="", field_length="",
                                  field_alias="",field_is_nullable= "NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
    
        flds = []
        for fld in field_map:
            flds.append(fld['FieldName'])
        flds.append(reporting_areas_ID_field)
        flds.append( "SHAPE@")
        flds.append(classified_layer_field_name)
    
        newRows = []
    
        with arcpy.da.UpdateCursor(_intersect, flds) as urows:
            for row in urows:
                val_fnd = False
                for field in reclass_map:
                    sql_state = field['Expression']
                    try:
    
    
                        for i in range (len( field_map)):
                            sql_state = sql_state.replace(field_map[i]['Expression'],str(row[i]))
    
                        if eval(sql_state) == True:
                            try:
                                if val_fnd == True:
                                    newRow = deepcopy(row)
                                    newRow[len(flds) - 1] = field['FieldName']
                                    newRows.append(newRow)
        
                                else:
                                    row[len(flds) - 1] = field['FieldName']
                                    val_fnd = True
                            except Exception, e:
                                print "       %s" % e                            
                    except Exception, e:
                        print "       WARNING: %s is not valid" % str(sql_state)
    
                if val_fnd == False:
    
                    row[len(flds) - 1] = 'NORECLASS'
                urows.updateRow(row)
            del row
            del urows
            if len(newRows) > 0 :
                with arcpy.da.InsertCursor(_intersect, flds) as irows:
    
                    for newRow in newRows:
                        irows.insertRow(newRow)
                del irows
        return _intersect
    
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "split_reclass",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "split_reclass",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:     
        _tempWorkspace = None
        flds = None
        val_fnd = None
        sql_state = None
        newRow = None
        newRows = None     
        
        del _tempWorkspace
        del flds
        del val_fnd
        del sql_state
        del newRow
        del newRows
        
        gc.collect()
#----------------------------------------------------------------------
def classified_pivot(classified_layer, classified_layer_field_name, reporting_areas_ID_field, count_field,summary_fields=''):
    
    _tempWorkspace = None       
    _freq = None 
    _pivot = None  
 
    try:    
        _tempWorkspace = env.scratchGDB
    
        _freq = os.path.join(_tempWorkspace ,Common.random_string_generator())
        _pivot = os.path.join(_tempWorkspace ,Common.random_string_generator())
    
        if not count_field in summary_fields and count_field != 'FREQUENCY':
            summary_fields = count_field if summary_fields =='' else summary_fields + ";" + count_field
    
        arcpy.Frequency_analysis(in_table=classified_layer, out_table=_freq,frequency_fields= reporting_areas_ID_field + ';' + classified_layer_field_name , summary_fields=summary_fields)
    
        arcpy.PivotTable_management(_freq, reporting_areas_ID_field,classified_layer_field_name , count_field, _pivot)
        deleteFC([_freq])
        return _pivot
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "JoinAndCalc",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "JoinAndCalc",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:  
        _tempWorkspace = None       
        _freq = None 
    
        del _tempWorkspace        
        del _freq
        
        gc.collect()
               
#----------------------------------------------------------------------
def copy_report_data_schema(reporting_areas, reporting_areas_ID_field,report_schema ,report_result, join_layer):

    _tempWorkspace = None     
    _reportCopy = None
    final_report = None
  
    try:
        _tempWorkspace = env.scratchGDB
        _reportCopy = Common.random_string_generator()    
        final_report = os.path.join(_tempWorkspace ,_reportCopy)
    
        # Process: Create a copy of the Reporting Areas for the summary info join
        arcpy.FeatureClassToFeatureClass_conversion(reporting_areas, _tempWorkspace, _reportCopy, "", reporting_areas_ID_field + ' "' + reporting_areas_ID_field + '" true true false 50 Text 0 0 ,First,#,' + reporting_areas +',' + reporting_areas_ID_field + ',-1,-1', "")
    
        # Process: Join the Areas to the pivot table to get a count by area
        arcpy.JoinField_management(final_report, reporting_areas_ID_field, join_layer, reporting_areas_ID_field, "#")
    
        # Process: Create a copy of the report layer
        if not os.path.isabs(report_result):
            report_result =os.path.abspath( report_result)
    
        if not os.path.isabs(report_schema):
            report_schema =os.path.abspath( report_schema)
       
        arcpy.Copy_management(report_schema,report_result,"FeatureClass")
        return final_report
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "classified_pivot",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "classified_pivot",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:  
        _tempWorkspace = None     
        _reportCopy = None
       
        del _tempWorkspace
        del _reportCopy
        
        gc.collect()
#----------------------------------------------------------------------
def calculate_average_report_results(report_result, reporting_areas_ID_field,report_copy, field_map  ,report_date_field,report_ID_field,average_field  ):
    fields = None
    strOnlineTime = None
    search_fields = None
    newrow = None
    try:
        fields = []
        for fld in field_map:
            fields.append(fld['FieldName'])
    
        fields.append(report_ID_field)
        fields.append(report_date_field)
        fields.append("SHAPE@")
    
        strOnlineTime = Common.online_time_to_string(Common.local_time_to_online(),dateTimeFormat)
        #strLocalTime = datetime.datetime.now().strftime(dateTimeFormat)
        search_fields = [average_field,reporting_areas_ID_field,"SHAPE@"]
    
        with arcpy.da.InsertCursor(report_result,fields) as irows:
            with arcpy.da.SearchCursor(report_copy,search_fields) as srows:
                for row in srows:
                    newrow = []    
                    for fld in field_map:
                        try:
                            newrow.append(eval(fld["Expression"].replace("{Value}", str(Common.noneToValue( row[0],0.0)))))
                        except Exception:
                            newrow.append(None)
                    newrow.append(row[1])
                    newrow.append(strOnlineTime)
                    newrow.append(row[2])
    
                    irows.insertRow(tuple(newrow)  )   
            del srows
        del irows
        return report_result
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "calculate_average_report_results",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "calculate_average_report_results",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally: 
        fields = None
        strOnlineTime = None
        search_fields = None
        newrow = None
        
        del fields
        del strOnlineTime
        del search_fields
        del newrow
        
        gc.collect()
        
#----------------------------------------------------------------------
def calculate_report_results(report_result, reporting_areas_ID_field,report_copy, reclass_map  ,report_date_field,report_ID_field ,exp ):
    appendString = None
    fields = None
    strOnlineTime = None
    try:
        appendString=""
        fields = []
        for fld in reclass_map:
            appendString +=   fld['FieldName'] + " \"\" true true false 8 Double 0 0 ,First,#," + report_copy + "," + fld['FieldName'] + ",-1,-1;"
            fields.append(fld['FieldName'])
    
        appendString +=  report_ID_field + " \"\" true true false 80 string 0 0 ,First,#," + report_copy + "," + reporting_areas_ID_field + ",-1,-1;"
    
    
        arcpy.Append_management(report_copy,report_result, "NO_TEST",appendString, "")
    
        strOnlineTime = Common.online_time_to_string(Common.local_time_to_online(),dateTimeFormat)
        #strLocalTime = datetime.datetime.now().strftime(dateTimeFormat)
        fields.append(report_date_field)
    
        with arcpy.da.UpdateCursor(report_result,fields) as urows:
            for row in urows:
                for u in range(len(fields) - 1):
                    row[u]= eval(exp.replace('{Value}', str(Common.noneToValue( row[u],0.0))))# {'__builtins__':{}}
    
                row[len(fields)-1] = strOnlineTime
                urows.updateRow(row)
            del urows
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "calculate_report_results",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "calculate_report_results",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    
    finally: 
        appendString = None
        fields = None
        strOnlineTime = None   
        
        del appendString
        del fields
        del strOnlineTime       
        gc.collect()
        
#----------------------------------------------------------------------
def copy_empty_report(reporting_areas, reporting_areas_ID_field,report_schema ,report_result,reclass_map  ,report_date_field,report_ID_field):
    
    _tempWorkspace = None
    _reportCopy = None
    _final_report = None
    appendString = None
    strOnlineTime = None
    fields = None
    
    try:
        _tempWorkspace = env.scratchGDB
    
        _reportCopy = Common.random_string_generator()
    
        _final_report = os.path.join(_tempWorkspace ,_reportCopy)
    
        # Process: Create a copy of the Reporting Areas for the summary info join
        arcpy.FeatureClassToFeatureClass_conversion(reporting_areas, _tempWorkspace, _reportCopy, "", reporting_areas_ID_field + ' "' + reporting_areas_ID_field + '" true true false 50 Text 0 0 ,First,#,' + reporting_areas +',' + reporting_areas_ID_field + ',-1,-1', "")
    
        # Process: Create a copy of the report layer
        arcpy.Copy_management(report_schema,report_result,"FeatureClass")
    
        appendString = report_ID_field + " \"\" true true false 80 string 0 0 ,First,#," + _final_report + "," + reporting_areas_ID_field + ",-1,-1;"
    
        arcpy.Append_management(_final_report,report_result, "NO_TEST",appendString, "")
    
        strOnlineTime = Common.online_time_to_string(Common.local_time_to_online(),dateTimeFormat)
        #strLocalTime = datetime.datetime.now().strftime(dateTimeFormat)
    
        fields = []
        for fld in reclass_map:
            fields.append(fld['FieldName'])
    
    
        fields.append(report_date_field)
    
        with arcpy.da.UpdateCursor(report_result,fields) as urows:
            for row in urows:
                for u in range(len(fields) - 1):
                    row[u]= str(Common.noneToValue( row[u],0.0))
    
    
                row[len(fields)-1] = strOnlineTime
                urows.updateRow(row)
            del urows
    
        deleteFC([_final_report])
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "copy_empty_report",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "copy_empty_report",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally: 
        _tempWorkspace = None
        _reportCopy = None
        _final_report = None
        appendString = None
        strOnlineTime = None
        fields = None  
        
        del _tempWorkspace
        del _reportCopy
        del _final_report
        del appendString
        del strOnlineTime
        del fields  
        
        gc.collect()
#----------------------------------------------------------------------
def shapeBasedSpatialJoin(TargetLayer, JoinLayer,JoinResult):
    _tempWorkspace = None     
    _targetCopyName = None
    _targetCopy = None
    _areaFieldName = None
    _idenResultLayer = None
   
    layDetails = None  
    _lenAreaFld = None
    
    try:
        if not arcpy.Exists( TargetLayer):
            raise ValueError(TargetLayer + " does not exist")
        if not arcpy.Exists( JoinLayer):
            raise ValueError(JoinLayer + " does not exist")
        # Local variables:
        _tempWorkspace = env.scratchGDB
    
        _targetCopyName = Common.random_string_generator()
        _targetCopy = os.path.join(_tempWorkspace ,_targetCopyName)
        #JoinResult = os.path.join(_tempWorkspace ,random_string_generator())
        _areaFieldName = Common.random_string_generator(size=12)
        _idenResultLayer ="polyIdenLayer"
    
        _lenAreaFld = "SHAPE_Area"
    
        layDetails = arcpy.Describe(TargetLayer)
        if layDetails.shapeType == "Polygon":
            _lenAreaFld = "Shape_Area"
        elif layDetails.shapeType == "Polyline":
            _lenAreaFld = "Shape_Length"
        else:
            return ""
        arcpy.FeatureClassToFeatureClass_conversion(TargetLayer,_tempWorkspace,_targetCopyName,"#","","#")
        # Process: Copy
        # Process: Add Field
        arcpy.AddField_management(_targetCopy, _areaFieldName, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
        # Process: Calculate Field
        arcpy.CalculateField_management(_targetCopy, _areaFieldName, "!" + _lenAreaFld +"!", "PYTHON_9.3", "")
    
        # Process: Identity
        arcpy.Identity_analysis(_targetCopy, JoinLayer, JoinResult, "ALL", "", "NO_RELATIONSHIPS")
    
        # Process: Make Feature Layer
        arcpy.MakeFeatureLayer_management(JoinResult, _idenResultLayer, "", "", "")
    
        # Process: Select Layer By Attribute
        arcpy.SelectLayerByAttribute_management(_idenResultLayer, "NEW_SELECTION", _lenAreaFld + " < .5 *  " + _areaFieldName)
    
        # Process: Delete Features
        arcpy.DeleteFeatures_management(_idenResultLayer)
    
        deleteFC([_targetCopy])

        return JoinResult 
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "shapeBasedSpatialJoin",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "shapeBasedSpatialJoin",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally: 
        _tempWorkspace = None     
        _targetCopyName = None
        _targetCopy = None
        _areaFieldName = None
        _idenResultLayer = None
      
        layDetails = None  
        _lenAreaFld = None     
        
        del _tempWorkspace 
        del _targetCopyName 
        del _targetCopy
        del _areaFieldName 
        del _idenResultLayer 
       
        del layDetails  
        del _lenAreaFld 
        
        gc.collect()    
#----------------------------------------------------------------------    
def JoinAndCalc(inputDataset, inputJoinField, joinTable, joinTableJoinField,copyFields, joinType="KEEP_ALL"):
    
    inputLayer = None   
    joinTableDesc = None
    joinName = None
    removeJoin = None
    tz = None
    dateExp = None
    exp = None

    try:

        inputLayer = "inputLayer"
        arcpy.MakeFeatureLayer_management (inputDataset, inputLayer)

        joinTableDesc = arcpy.Describe(joinTable)
        joinName = str(joinTableDesc.name)
        arcpy.AddJoin_management(inputLayer, inputJoinField, joinTable, joinTableJoinField,joinType)
        removeJoin = True

        tz = time.timezone # num of seconds to add to GMT based on current TimeZone

        for copyField in copyFields:
            if len(copyField) == 3:
                dateExp = "import time\\nimport datetime\\nfrom time import mktime\\nfrom datetime import datetime\\ndef calc(dt):\\n  return datetime.fromtimestamp(mktime(time.strptime(str(dt), '" + str(copyField[2]) + "')) +  time.timezone)"
                exp =  'calc(!' + joinName +'.' + copyField[0] + '!)'
                arcpy.CalculateField_management(inputLayer,copyField[1], exp, 'PYTHON_9.3', dateExp)

            else:
                arcpy.CalculateField_management(inputLayer,copyField[1], '!' + joinName +'.' + copyField[0] + '!', "PYTHON_9.3", "")

            print copyField[1] + " Calculated from " + copyField[0]

        arcpy.RemoveJoin_management(inputLayer,joinName)
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "JoinAndCalc",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "JoinAndCalc",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        inputLayer = None   
        joinTableDesc = None
        joinName = None
        removeJoin = None
        tz = None
        dateExp = None
        exp =  None
        
        del inputLayer   
        del joinTableDesc
        del joinName 
        del removeJoin
        del tz 
        del dateExp
        del exp     
#----------------------------------------------------------------------            
def fieldsToFieldArray(featureclass):
    """fieldsToFieldArray(featureclass)

       Converts fields to a list

         featureclass(String):
       The specified feature class or table whose fields will be returned.

    """
    fieldList = None
    try:
        fieldList = arcpy.ListFields(featureclass)
        returnFields = []
        for field in fieldList:
            returnFields.append(field.name)
                    
        return returnFields
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
            "function": "fieldsToFieldArray",
            "line": line,
            "filename":  filename,
            "synerror": synerror,
        }
                          )
    finally:
        fieldList = None
        
        del fieldList
        
        gc.collect()
#----------------------------------------------------------------------    
def FieldExist(featureclass, fieldNames):
    """FieldExist(dataset, [fieldNames])

       Determines if the array of fields exist in the dataset

         dataset(String):
       The specified feature class or table whose indexes will be returned.

         fieldNames{Array}:
       The the array of field name to verify existance."""
    fieldList = None
    fndCnt = None  
   
    try:
        fieldList = arcpy.ListFields(featureclass)
        fndCnt = 0
        for field in fieldList:
            if field.name in fieldNames:
                fndCnt = fndCnt + 1

            if fndCnt >0 :
                return True
            del field
        if fndCnt != len(fieldNames):
            return False

    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
            "function": "FieldExist",
            "line": line,
            "filename":  filename,
            "synerror": synerror,
        }
                          )
    finally:
        fieldList = None
        fndCnt = None
        
        del fieldList 
        del fndCnt
        
        gc.collect()
#----------------------------------------------------------------------  
def calc_field(inputDataset,field_map,code_exp,result_field):
    
    res = None  
    sqlState = None
    replaceValList = None
    newList = None
    
    try:

        replaceValList = []
        newList =[]
        for fld in field_map:
            newList.append(fld['FieldName'])
            replaceValList.append (fld['ReplaceValue'])
        newList.append(result_field)
        with arcpy.da.UpdateCursor(inputDataset, newList) as cursor:

            for row in cursor:
                sqlState = code_exp
                try:
                    for i in range(0,len(replaceValList)):
                        sqlState = sqlState.replace(replaceValList[i],str(row[i]))

                    res = eval(sqlState)
                    row[len(newList) -1] = res
                    cursor.updateRow(row)

                except Exception:
                    cursor.deleteRow()
            del row
            del cursor
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "JoinAndCalc",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )    
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
            "function": "calc_field",
            "line": line,
            "filename":  filename,
            "synerror": synerror,
        })
    finally:
        res = None  
        sqlState = None
        replaceValList = None
        newList = None
        
        del res  
        del sqlState
        del replaceValList
        del newList
        
        gc.collect()
#----------------------------------------------------------------------  
def calculate_age_field(inputDataset,field,result_field):
    newList = None   
    try:

        newList =[field,result_field]
        with arcpy.da.UpdateCursor(inputDataset, newList) as cursor:


            for row in cursor:
                if row[0] == None:
                    cursor.deleteRow()
                else:
                    row[1] = datetime.datetime.now().year - row[0].year
                    cursor.updateRow(row)
            del row
        del cursor
    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
                    "function": "JoinAndCalc",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )    
    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
            "function": "calculate_age_field",
            "line": line,
            "filename":  filename,
            "synerror": synerror,
        })
    finally:
        newList = None
        
        del newList
        
        gc.collect()

#----------------------------------------------------------------------  
def calculate_inline_stats(inputDataset,fields,result_field,stats_method):
    """calculate_inline_stats(inputDataset,(field1, field2,..),resultField,<Min, Max, Sum, Mean>)

    Calculates stats on the input table

     dataset(String):
    The specified feature class or table

     fields(field1,field2,..):
    List of fields to perform stats on

     result_field:
    Field to store the results on

     stats_method:
    Type of stats to perform
    """
    lstLen = None
    newList = None
    cnt  = None
    val = None  
    minVal = None  
    maxVal = None  
    try:

        lstLen = len(fields)
        newList =deepcopy(fields)
        newList.append(result_field)
        with arcpy.da.UpdateCursor(inputDataset, tuple(newList)) as cursor:


            for row in cursor:
                row.pop(lstLen)
                if  stats_method.upper() == "AVERAGE" or  stats_method.upper() == "AVG" or  stats_method.upper() == "MEAN":
                    cnt = 0
                    val = 0
                    for i in row:
                        if i is not None:
                            cnt += 1
                            val += i
                    row.append(val/cnt)
                elif  stats_method.upper() == "MIN" or  stats_method.upper() == "MINIMUM":
                    minVal = min(i for i in row if i is not None)
                    row.append(minVal)
                elif  stats_method.upper() == "MAX" or  stats_method.upper() == "MAXIMUM":
                    maxVal = max(i for i in row if i is not None)
                    row.append(maxVal)
                cursor.updateRow(row)
            del row
            del cursor

    except:
        line, filename, synerror = Common.trace()
        raise ReportToolsError({
            "function": "calculate_inline_stats",
            "line": line,
            "filename":  filename,
            "synerror": synerror,
        })
    finally:
        lstLen = None
        newList = None
        cnt  = None
        val = None  
        minVal = None  
        maxVal = None 
        
        del lstLen 
        del newList 
        del cnt 
        del val 
        del minVal   
        del maxVal  

        gc.collect()
        
#----------------------------------------------------------------------  
def deleteFC(in_datasets):

    for in_data in in_datasets:
        try:
            if in_data is not None:
                if arcpy.Exists(dataset=in_data):
                    arcpy.Delete_management(in_data=in_data)
       
        except Exception:
            print "Unable to delete %s" % in_data

