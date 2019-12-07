pipeline {
   agent any

   parameters{
      string(name: 'NumberOfDays',
      defaultValue: '1',
      description: 'backdated days')
   
      string(name: 'BaseFileName',
      defaultValue: 'base.xlsx',
      description: 'base file for consolidatiuon')
   
      string(name: 'NewFileName',
      defaultValue: 'new.xlsx',
      description: 'New file with latest status')
   }

   parameters{
      string(name: 'AssignmentFileName',
      defaultValue: 'assignment_ID.xlsx',
      description: 'Assignment Sheet latest')
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

            echo '${params.NumberOfDays}'
            sh 'pip install -r requirement.txt'
            sh 'python ./excelprocessor.py "./files/${BaseFileName}" "./files/${NewFileName}" "./files/a${AssignmentFileName}" "./files/" ${NumberOfDays} '

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