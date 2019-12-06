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
            sh 'ls -latr'
            sh 'cd files'
            sh 'ls -latr'
            sh 'cd ..'

         }

      }

      stage('Process consolidation') {


         steps {
            sleep(40)
            sh 'pip install -r requirement.txt'
            sh 'python ./excelprocessor.py "/files/base.xlsx" "/files/new.xlsx" "/files/assignmentID.xlsx" "/files/" 4'

         }

      }

  }

}