pipeline {
   agent any

   stages {

    stage('Checkout') {
         steps {
        git 'https://github.com/sridharkidambi/beelineProcessor'

        }
       }
      stage('download files from s3') {


         steps {

            sh 'aws s3 sync s3://beelineprocess  files'

         }

      }

      stage('Process consolidation') {


         steps {

            sh 'pip install -r requirement.txt'
            sh 'apt-get install python-tk'
            sh 'python ./excelprocessor.py "/files/base.xlsx" "/files/new.xlsx" "/files/assignment_ID.xlsx" "/files/" 4'

         }

      }

  }

}