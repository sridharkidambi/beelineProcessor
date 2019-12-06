pipeline {
   agent any

   parameters{
      string(name: 'NumberOfDays',
      defaultValue: '1',
      description: 'backdated days')
   }

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
            sh 'python ./excelprocessor.py "./files/base.xlsx" "./files/new.xlsx" "./files/assignmentID.xlsx" "./files/" ${params.NumberOfDays}'

         }

      }


      stage('Upload to S3') {


         steps {
            
            sh 'aws s3 cp "./files/CONSOLIDATED_BASE.xlsx" s3://beelineprocess'

         }

      }

      stage('Send email') {


         steps {
            
            sh 'ls -latr'

         }

      }

  }

}