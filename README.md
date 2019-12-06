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


### Step 3(only for once in a laptop):
 run the following command (only for the first time)
 
#### pip install -r requirement.txt
 
 the command will download the needed libraries as shown below(will take sometime)
 
 ![Capture](https://user-images.githubusercontent.com/8262606/68460640-638a9880-022e-11ea-9655-4198570edd3d.PNG)
 
 ### Step 4:
 
 run the below  command . for execution 
 
 #### python excelprocessor.py  “base file path with filename” “new file path with filename” “assignment file path with filename” “output file path with filename” count of days
 
#### substitution ex:  'base file path with filename': "c:\beeline\base.xlsx"
 
 ### Step 5:
 
 Output will be generated as CONSOLIDATED_BASE.xlsx in the path <output file path with filename> mentioned at Step 4.
 
 open the file(CONSOLIDATED_BASE.xlsx ) and do the following format changes
 
 1.Select the columns from SubmittedDate until WeekendDate
 
 <img width="629" alt="Screenshot 2019-12-02 at 4 04 00 PM" src="https://user-images.githubusercontent.com/8262606/69952763-e0ebb500-151d-11ea-884d-c3249822d189.png">
<img width="660" alt="Screenshot 2019-12-02 at 4 04 37 PM" src="https://user-images.githubusercontent.com/8262606/69952792-ee08a400-151d-11ea-8d2e-6d074720cc2b.png">
format: [$-en-US]d-mmm-yy;@
<img width="500" alt="Screenshot 2019-12-02 at 4 05 41 PM" src="https://user-images.githubusercontent.com/8262606/69952855-11cbea00-151e-11ea-9f28-edad81fca372.png">
<img width="588" alt="Screenshot 2019-12-02 at 4 05 51 PM" src="https://user-images.githubusercontent.com/8262606/69952893-27411400-151e-11ea-82ad-e0cf8b2b7bc7.png">

#### For Month:
<img width="215" alt="Screenshot 2019-12-02 at 4 04 52 PM" src="https://user-images.githubusercontent.com/8262606/69952946-48096980-151e-11ea-8f35-aa3330962971.png">
<img width="655" alt="Screenshot 2019-12-02 at 4 05 04 PM" src="https://user-images.githubusercontent.com/8262606/69953010-640d0b00-151e-11ea-811a-f7b73f313e5a.png">


Format: [$-en-US]mmm/yy;@
<img width="500" alt="Screenshot 2019-12-02 at 4 05 41 PM" src="https://user-images.githubusercontent.com/8262606/69952855-11cbea00-151e-11ea-9f28-edad81fca372.png">
<img width="588" alt="Screenshot 2019-12-02 at 4 05 51 PM" src="https://user-images.githubusercontent.com/8262606/69952893-27411400-151e-11ea-82ad-e0cf8b2b7bc7.png">
 


