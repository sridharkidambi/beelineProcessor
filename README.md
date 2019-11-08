# BeelineProcessor

**** This documentation is for persons holding a Wipro Windows laptop and having adminstrative rights.****

### Step 1:
Login Mywipro and navigate to Raise the software request in mywipro->myrequest->IT request->Software  

<img width="1678" alt="Screenshot 2019-11-08 at 1 07 41 PM" src="https://user-images.githubusercontent.com/8262606/68458499-f9bbc000-0228-11ea-9c0f-1da5db61d504.png">

Now raise the software request for below:

![pic2](https://user-images.githubusercontent.com/8262606/68460569-35a55400-022e-11ea-8949-f89d55305eb0.PNG)


**** note: wait for the software to auto download to your systems ****

### Step 2:
1.Download the code( https://github.com/sridharkidambi/beelineProcessor)  to a path  and open a command prompt up the sourcecode folder level(beelineProcessor)

2.Download the basefile,newfile and the assignmentID file to a path

3.Open the new sheet downloaded , and modify the column J as 'Date.1' as mentioned in the below pictures
 <img width="131" alt="Screenshot 2019-11-08 at 1 40 24 PM" src="https://user-images.githubusercontent.com/8262606/68460376-c3347400-022d-11ea-9436-dce02815ca8e.png">

### Step 3:
 run the following command (only for the first time)
 
#### pip install -r requirement.txt
 
 the command will download the needed libraries as shown below(will take sometime)
 
 ![Capture](https://user-images.githubusercontent.com/8262606/68460640-638a9880-022e-11ea-9655-4198570edd3d.PNG)
 
 ### Step 4:
 
 run the below  command . for execution 
 
 #### python excelprocessor.py  “base file path with filename” “new file path with filename” “assignment file path with    filename” “output file path” 
 
#### substitution ex:  'base file path with filename': "c:\\\beeline\\base.xlsx"
 
 ### Step 5:
 
 Output will be generated as CONSOLIDATED_BASE.xlsx in the path <output file path> mentioned at Step 4.
 


