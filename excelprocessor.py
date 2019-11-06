import pandas as pd
import pandasql as psql
import boto3
import timeit
import datetime
from datetime import timedelta
from pympler import muppy
from pympler import summary
from io import StringIO
import s3fs
import xlrd
import xlsxwriter
from decimal import Decimal
import math
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np

# import StringIO
# import cherrypy
# import dowser

def formatter(x):
    return '"""$"#,##0.00""'.format(x)

def excel_date(date1):
    temp=datetime.datetime.strptime('19000101', '%Y%m%d')
    delta=date1-temp
    total_seconds = delta.days +2 #* 86400 + delta.seconds
    return total_seconds
def usingchuck():
    DAYS_COUNT=16
    print((datetime.datetime.now()+ timedelta(days=-DAYS_COUNT)).strftime('%d-%b-%y'))
    # return
    query_string  = 'select distinct `SOW Number`,LOB,Domain,`Supplier Name`,Assignment  from dt_base '
    query_string1  = 'select distinct month  from dt_base_cpy '
    print('******Read the assignment  file**********')
    dt_assignt=pd.read_excel('/Users/sridharkidambi/aarthi/assignment_ID.xlsx',index_col=None,header=0,error_bad_lines=False, ignore_index = True)
    # print(dt_assignt)

    # return

    print('******Read the base copy file**********')
    dt_base=pd.read_excel('/Users/sridharkidambi/aarthi/base.xlsx',sheet_name='Sheet1',index_col=None,header=0,error_bad_lines=False,date_parser=lambda ts: pd.to_datetime(ts, '%Y-%m-%d %H:%M:%S',
                                                       coerce=True), ignore_index = True)
    dt_base_cpy=dt_base.copy()
    dt_base_cpy['Row_Modified']='NA'
    # print(dt_base_cpy)
    # return
    uniq_items = psql.sqldf(query_string, locals())
    print('********Lookup tables********')
    # print(uniq_items)

    # return

    print('*******Read the new file*********')
    dt_new=pd.read_excel('/Users/sridharkidambi/aarthi/new.xlsx',index_col=None,header=0,error_bad_lines=False)
    


    print('*******Prepare  the new file Columns*********')
    dt_new['Amount']=''
    # dt_new['DID']=''
    dt_new['ACTION REQUIRED']='TBD'
    dt_new['Ownership']='TBD'
    dt_new['Action Pending With']='TBD'
    dt_new['Category']='TBD'
    dt_new['combo']=''
    dt_new['Row_Modified']='NA'
    dt_new.insert(2,'DID','')
    dt_new.insert(3,'SOW Number','')
    dt_new.insert(4,'LOB','')
    dt_new.insert(5,'Domain','')
    dt_new.insert(6,'Supplier Name','')
    dt_new.insert(8,'Approver Name','')
    dt_new.insert(9,'Wipro Manager','')
    dt_new.insert(11,'Submission Category','')

    dt_new.rename(columns={'Date': 'Week Start Date','Date.1': 'Weekend Date','ID': 'Assignment','Name': 'Timesheet Status','Rejected Date': 'Rejected'},inplace=True)
    subst_dt_new =dt_new[(pd.to_datetime(dt_new['Submitted Date']) >= (datetime.datetime.now()+ timedelta(days=-DAYS_COUNT)).strftime('%d-%b-%y')) | ((pd.to_datetime(dt_new["Rejected"])) >= (datetime.datetime.now()+ timedelta(days=-DAYS_COUNT)).strftime('%d-%b-%y')) | (pd.to_datetime(dt_new["Approved Date and Time"])>= (datetime.datetime.now()+ timedelta(days=-DAYS_COUNT)).strftime('%d-%b-%y'))]
    # print(len(subst_dt_new.index))
    # return
    # for item in dt_base.index:
    #     print('b4')
    #     print(dt_base_cpy['combo'][item])
    #     # dt_base_cpy['combo'][item]=str(dt_base_cpy['Assignment'][item]) + str(dt_base_cpy['Project Number'][item])+ str(excel_date(dt_base_cpy['Weekend Date'][item]))+ str(dt_base_cpy['Amount'][item])
    #     print('after')
    #     print(dt_base_cpy['combo'][item])
    #     print(str(dt_base_cpy['Assignment'][item]))
    #     print(str(dt_base_cpy['Project Number'][item]))
    # return
    for item in subst_dt_new.index:
        
        assignt_subst_df=dt_assignt[(dt_assignt["ID"]==subst_dt_new['Assignment'][item])]
        assignt_subst_df.reset_index(drop=True, inplace=True)
        # print(len(assignt_subst_df.index))
        # return
        base_subst_df=dt_base[(dt_base["Project Number"]==subst_dt_new['Project Number'][item]) & (dt_base["Assignment"]==subst_dt_new['Assignment'][item] )]
        
        if(len(base_subst_df.index)>0):
                base_subst_df.reset_index(drop=True, inplace=True)
                subst_dt_new['SOW Number'][item]=base_subst_df['SOW Number'][0]
                subst_dt_new['LOB'][item]=base_subst_df['LOB'][0]
                subst_dt_new['Domain'][item]=base_subst_df['Domain'][0]
                subst_dt_new['Supplier Name'][item]=base_subst_df['Supplier Name'][0]
                subst_dt_new['DID'][item]=base_subst_df['DID'][0]
                if(len(assignt_subst_df.index)>0):
                    subst_dt_new['Approver Name'][item]=assignt_subst_df['Name'][len(assignt_subst_df.index)-1]
                # print(subst_dt_new[item])
                
                subst_dt_new['Amount'][item]=subst_dt_new['Units'][item] * subst_dt_new['RT Rate'][item]
                val_int = int(subst_dt_new['Amount'][item])
                val_fract = (subst_dt_new['Units'][item] * subst_dt_new['RT Rate'][item]) - val_int
                # print((base_subst_df['Units'][0] * base_subst_df['RT Rate'][0]))
                if(val_fract>0.0):
                    subst_dt_new['Amount'][item]=subst_dt_new['Units'][item] * subst_dt_new['RT Rate'][item]
                    subst_dt_new['Amount'][item]=round(subst_dt_new['Amount'][item],2)
                else:
                    subst_dt_new['Amount'][item]=val_int

                subst_dt_new['combo'][item]=str(subst_dt_new['Assignment'][item]) + str(subst_dt_new['Project Number'][item])+ str(excel_date(subst_dt_new['Weekend Date'][item]))+ str(subst_dt_new['Amount'][item])
                if((str(subst_dt_new['Timesheet Status'][item]).strip()=='Locked') | ((str(subst_dt_new['Timesheet Status'][item]).strip()=='Approved'))):
                    subst_dt_new['Timesheet Status'][item]='Payment pending'
                elif((str(subst_dt_new['Timesheet Status'][item]).strip()) == 'Submitted'):
                    subst_dt_new['Timesheet Status'][item]='Approval pending'
                subst_dt_new['ACTION REQUIRED'][item]=subst_dt_new['Timesheet Status'][item]
                if(((str(subst_dt_new['Timesheet Status'][item]).strip()) == 'Payment pending')| ((str(subst_dt_new['Timesheet Status'][item]).strip()) == 'Approval pending')):
                    subst_dt_new['Ownership'][item]='capone'
                else:
                    subst_dt_new['Ownership'][item]='wipro'
        else:
                if(len(assignt_subst_df.index)>0):
                    subst_dt_new['Approver Name'][item]=assignt_subst_df['Name'][len(assignt_subst_df.index)-1]
                # print(subst_dt_new[item])
                
                subst_dt_new['Amount'][item]=subst_dt_new['Units'][item] * subst_dt_new['RT Rate'][item]
                val_int = int(subst_dt_new['Amount'][item])
                val_fract = (subst_dt_new['Units'][item] * subst_dt_new['RT Rate'][item]) - val_int
                # print((base_subst_df['Units'][0] * base_subst_df['RT Rate'][0]))
                if(val_fract>0.0):
                    subst_dt_new['Amount'][item]=subst_dt_new['Units'][item] * subst_dt_new['RT Rate'][item]
                    # print(subst_dt_new['Amount'][item])
                    subst_dt_new['Amount'][item]=round(subst_dt_new['Amount'][item],2)
                    # print(subst_dt_new['Amount'][item])
                else:
                    subst_dt_new['Amount'][item]=val_int
                subst_dt_new['combo'][item]=str(subst_dt_new['Assignment'][item]) + str(subst_dt_new['Project Number'][item])+ str(excel_date(subst_dt_new['Weekend Date'][item]))+ str(subst_dt_new['Amount'][item])
                if((str(subst_dt_new['Timesheet Status'][item]).strip()=='Locked') | ((str(subst_dt_new['Timesheet Status'][item]).strip()=='Approved'))):
                    subst_dt_new['Timesheet Status'][item]='Payment pending'
                elif((str(subst_dt_new['Timesheet Status'][item]).strip()) == 'Submitted'):
                    subst_dt_new['Timesheet Status'][item]='Approval pending'
                subst_dt_new['ACTION REQUIRED'][item]=subst_dt_new['Timesheet Status'][item]
                if(((str(subst_dt_new['Timesheet Status'][item]).strip()) == 'Payment pending')| ((str(subst_dt_new['Timesheet Status'][item]).strip()) == 'Approval pending')):
                    subst_dt_new['Ownership'][item]='capone'
                else:
                    subst_dt_new['Ownership'][item]='wipro'
        # print(str(subst_dt_new['Last Name, First Name Middle Name'][item])+ '---'+ str(subst_dt_new['Project Number'][item])+ '---'+ str(subst_dt_new['Assignment'][item]))
        subst_dt_new['Row_Modified'][item]='New'
        
        # return
        # else:

                # print('%%%%%%%%%%%%%%%%   BASE SUBSET %%%%%%%%%%%%%%%%   ')
                # print('%%%%%%%%%%%%%%%%   BASE SUBSET %%%%%%%%%%%%%%%%   ')

       
    mod_subst_dt_new =subst_dt_new[(subst_dt_new['Row_Modified'] == 'New')]
    # print(len(mod_subst_dt_new.index))
    # return
    # print(dt_base["combo"])
    
    print ('^^^^^^^^^^^^^^^^^^ Process updates and inserts to Base file ^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    
    irowsModified=0
    iRowsAdded=0
    itotal=0
    iUnits_Zero=0
    for item in mod_subst_dt_new.index:
        # print(Decimal(mod_subst_dt_new['combo'][item]))
        # print(type(mod_subst_dt_new['combo'][item]))
        # print(Decimal(mod_subst_dt_new['combo'][item]))
        # print('combo values:')
        # print(str(mod_subst_dt_new['combo'][item]))
        mod_base_subst_df=dt_base_cpy[dt_base_cpy["combo"] == str(mod_subst_dt_new['combo'][item])]
        

        if(mod_base_subst_df.index.values.size>0):
            if (mod_subst_dt_new['Timesheet Status'][item]=='Payment pending'):
                mod_subst_dt_new['Action Pending With'][item]= 'AP TEAM'
                
            if (mod_subst_dt_new['Timesheet Status'][item]=='Approval pending'):
                mod_subst_dt_new['Action Pending With'][item]= mod_subst_dt_new['Approver Name'][item]
            mod_base_subst_df['Row_Modified'][item]='Modified'

                # """$"#,##0.00""
        # print(mod_base_subst_df.index.values.tolist())
        # print('my index values are: ')
        # return
        # idx = dt_base.index[dt_base['combo']== str(Decimal(mod_subst_dt_new['combo'][item]))]
        # print('my index values are: ')
        # print(idx[0])
        # print('my index is')
        # print(mod_base_subst_df.index.values.size)
        # return
        # mod_base_subst_df=dt_base[round(float(dt_base["combo"]),2)== str(round(float(mod_subst_dt_new['combo'][item]),2))]
        # print(len(mod_base_subst_df.index))
        # print(mod_base_subst_df)
        if(mod_base_subst_df.index.values.size>0):
            index_value=mod_base_subst_df.index.values.tolist()[0]
            irowsModified=irowsModified+1
            itotal=itotal+1
            # dt_base_cpy[index_value]['Row_Modified'] = mod_subst_dt_new['Row_Modified'][item]
            dt_base_cpy.at[index_value, 'Row_Modified'] = 'Modified'
            dt_base_cpy.at[index_value, 'Timesheet Status'] = mod_subst_dt_new['Timesheet Status'][item]
            dt_base_cpy.at[index_value, 'Submitted Date'] = (mod_subst_dt_new['Submitted Date'][item]).strftime('%d-%b-%y')
            # dt_base_cpy.at[index_value, 'Rejected'] = (mod_subst_dt_new['Rejected'][item]).strftime('%d-%b-%y')
            dt_base_cpy.at[index_value, 'Week Start Date'] = (mod_subst_dt_new['Week Start Date'][item]).strftime('%d-%b-%y')
            dt_base_cpy.at[index_value, 'Weekend Date'] = (mod_subst_dt_new['Weekend Date'][item]).strftime('%d-%b-%y')
            dt_base_cpy.at[index_value, 'ACTION REQUIRED'] = mod_subst_dt_new['ACTION REQUIRED'][item]
            dt_base_cpy.at[index_value, 'Ownership'] = mod_subst_dt_new['Ownership'][item]
            dt_base_cpy.at[index_value, 'Category'] = mod_subst_dt_new['Category'][item]
            dt_base_cpy.at[index_value, 'Action Pending With'] = mod_subst_dt_new['Action Pending With'][item]
            # Arthi request to copy the units amount from the new sheet
            dt_base_cpy.at[index_value, 'Units'] = mod_subst_dt_new['Units'][item]
            dt_base_cpy.at[index_value, 'RT Rate'] = mod_subst_dt_new['RT Rate'][item]
            dt_base_cpy.at[index_value, 'Amount']=mod_subst_dt_new['Units'][item] * mod_subst_dt_new['RT Rate'][item]
            val_int = int(dt_base_cpy.at[index_value, 'Amount'])
            val_fract = (mod_subst_dt_new['Units'][item] * mod_subst_dt_new['RT Rate'][item]) - val_int
            if(val_fract>0.0):
                    dt_base_cpy.at[index_value, 'Amount']=mod_subst_dt_new['Units'][item] * mod_subst_dt_new['RT Rate'][item]
                    dt_base_cpy.at[index_value, 'Amount']=round(dt_base_cpy.at[index_value, 'Amount'],2)
            else:
                    dt_base_cpy.at[index_value, 'Amount']=val_int
            # Arthi request to copy the units amount from the new sheet END
        else:
            mod_subst_dt_new['Row_Modified'][item]='Added'
            itotal=itotal+1
            # mod_subst_dt_new['Month'][item]=str(mod_subst_dt_new['Month'][item]) + '/' + '01'  +'/' + str(mod_subst_dt_new['Year'][item])
            mod_subst_dt_new['Month'][item]=str(mod_subst_dt_new['Month'][item]) + '/'  + str(mod_subst_dt_new['Year'][item])
            # print(mod_subst_dt_new['Month'][item])
            if(mod_subst_dt_new['Units'][item] != 0):
                iRowsAdded=iRowsAdded+1
                dt_base_cpy= dt_base_cpy.append(mod_subst_dt_new.loc[item] , ignore_index = True)
            else:
                iUnits_Zero=iUnits_Zero+1
    # return
    print('Rws Added : ' + str(iRowsAdded))
    print('Rws Modified : ' + str(irowsModified))
    print('Skipped with iUnits_Zero are  : ' + str(iUnits_Zero))
    print('All Rws in Total  : ' + str(itotal))
    # try:
    dt_base_cpy['Submitted Date']=pd.to_datetime(dt_base_cpy['Submitted Date']).dt.strftime('%d-%b-%y')
    dt_base_cpy['Weekend Date']=pd.to_datetime(dt_base_cpy['Weekend Date']).dt.strftime('%d-%b-%y')
    dt_base_cpy['Week Start Date']=pd.to_datetime(dt_base_cpy['Week Start Date']).dt.strftime('%d-%b-%y')
    dt_base_cpy['Rejected']=pd.to_datetime(dt_base_cpy['Rejected']).dt.strftime('%d-%b-%y')
    dt_base_cpy['Approved Date']=dt_base_cpy['Approved Date'].astype(str)
    dt_base_cpy['Approved Date']=dt_base_cpy['Approved Date'].apply(lambda x : None if x=="NaT" else x)
    dt_base_cpy['Approved Date']=pd.to_datetime(dt_base_cpy['Approved Date']).dt.strftime('%d-%b-%y')
    dt_base_cpy['Month']=pd.to_datetime(dt_base_cpy['Month'], errors = 'coerce').dt.strftime('%m/%y')
    # dt_base_cpy = dt_base_cpy.replace(np.na, '', regex=True)
    # dt_base_cpy['Month']=pd.to_datetime(dt_base_cpy.loc[:,'Month'],format="%m/%y")

    # catch  ex:
    # return
    # print(dt_base_cpy['Month'])
    # return 
    # m = dt_base_cpy['Month'].str.isdigit()
    # print(m)
    # dt_base_cpy.loc[m, 'Month'] = dt_base_cpy.loc[m, 'Month'].astype(int).apply(from_excel_ordinal)
    # dt_base_cpy['Month']=pd.to_datetime(dt_base_cpy['Month']).dt.strftime('%d-%b-%y')
    writer = pd.ExcelWriter('/Users/sridharkidambi/aarthi/CONSOLIDATED_BASE.xlsx', engine='xlsxwriter' )
    dt_base_cpy.to_excel(writer, sheet_name='Sheet1', index=False )
    # workbook  = writer.book
    # worksheet = writer.sheets['CONSOLIDATED_BASE']
    # date_format = workbook.add_format({'num_format': '%d-%b-%y'}) 
    # worksheet.set_column('A:A', 15,date_format)
    writer.save()
    # dt_base_cpy.plot(x ='Units', y='Units', color='blue',kind = 'scatter')
    # plt.show()
    return

    
    # dfObj = pd.DataFrame()
    for item in dt_new.index:
        # new_lst.append(item[0])
        # print(type(item))
        # print(dt_new['Submitted Date'][item])
        # print('******************************')
        
        subst_df=dt_assignt[(dt_assignt["ID"]==dt_new['Assignment'][item])] # & (dt_assignt["Name"]=='Haugen, Gregory')
        print('**********************subst_df***********************')
        print(subst_df)
        print(len(subst_df.index))
        # break
        # print(type(dt_new['Submitted Date'][item]))
        if ((dt_new['Submitted Date'][item]> (datetime.datetime.now()+ timedelta(days=-700))) | (dt_new['Approved Date and Time'][item]> (datetime.datetime.now()+ timedelta(days=-700)))| (dt_new['Rejected Date'][item]> (datetime.datetime.now()+ timedelta(days=-700)))):
            print ('valid')
            # print(dt_new['Assignment'][item])
            # print(dt_base["Assignment"])
            # print(dt_new['Project Number'][item])
            # print(dt_base["Project Number"])
            base_subst_df=dt_base[(dt_base["Project Number"]==dt_new['Project Number'][item]) &(dt_base["Assignment"]==dt_new['Assignment'][item] )] 
            # print('print base subset length')
            # print(base_subst_df.count)
            # print('print base subset length ends')
            if(len(base_subst_df.index)>0):
                base_subst_df.reset_index(drop=True, inplace=True)
                dt_new['SOW Number'][item]=base_subst_df['SOW Number'][0]
                dt_new['LOB'][item]=base_subst_df['LOB'][0]
                dt_new['Domain'][item]=base_subst_df['Domain'][0]
                dt_new['Supplier Name'][item]=base_subst_df['Supplier Name'][0]
                dt_new['ACTION REQUIRED'][item]=dt_new['Timesheet Status'][0]
                dt_new['Amount'][item]=base_subst_df['Units'][0] * base_subst_df['RT Rate'][0]
                dt_new['Combo'][item]=str(dt_new['Assignment'][item]) + str(dt_new['Project Number'][item])+ str(excel_date(dt_new['Weekend Date'][item]))+ str(dt_new['Amount'][item])
                print('timesheet status value')
                print(dt_new['Timesheet Status'][item])
                print('timesheet status value ends')
                if(dt_new['Timesheet Status'][item]=='Locked' | dt_new['Timesheet Status'][item]=='Approved'):
                    dt_new['Timesheet Status'][item]='Payment pending'
                if(dt_new['Timesheet Status'][item]=='Submitted'):
                    dt_new['Timesheet Status'][item]='Approval pending'
                print('%%%%%%%%%%%%%%%%   BASE SUBSET %%%%%%%%%%%%%%%%   ')
                # print(base_subst_df.loc[0])
                # print(excel_date(base_subst_df['Weekend Date'][0]))
                # print('$$$$$$$$$$$$$$')
                # print(dt_new.loc[item])
            # break
            # dfObj.insert(dt_new[item])
            # dfObj.append(dt_new[item])
        # else:
        #     print ('not-valid')
        # print(item[0])
        # print(item[1])
        # print(item[2])
        # break
    print('*********printing************')
    # print(type(new_lst))
    # print(dfObj)


if __name__=='__main__':
    strt1=datetime.datetime.now()
    usingchuck()
    strt2=datetime.datetime.now()
    print(strt2-strt1)
    
    # all_objects = muppy.get_objects()
    # print(len(all_objects))
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)
    # start(8081)

    # strt1=datetime.datetime.now()
    # print(datetime.time)
    # usingNochuck()
    # strt2=datetime.datetime.now()
    # print(strt2-strt1)
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)
# def start(port):
#     cherrypy.tree.mount(dowser.Root())
#     cherrypy.config.update({
#         'environment': 'embedded',
#         'server.socket_port': port
#     })
#     cherrypy.engine.start()
