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
   
      string(name: 'AssignmentFileName',
      defaultValue: 'assignment_ID.xlsx',
      description: 'Assignment Sheet latest')

      string(name: 'JENKINS_ACCESS_KEY_ID',
      defaultValue: 'AKIAXXFZRLIBYHFAR3A2',
      description: 'JENKINS_ACCESS_KEY_ID')

      password(name: 'JENKINS_SECRET_ACCESS_KEY',
      defaultValue: 'X1JZ/DjO9mh5FI2SLBIf1Dh6NaDDF+T/1V/4QYgQ',
      description: 'JENKINS_SECRET_ACCESS_KEY')

      string(name: 'DEFAULT_REGION',
      defaultValue: 'us-east-1',
      description: 'DEFAULT_REGION')

     
   }

   stages {

    stage('Checkout') {
         steps {
        git 'https://github.com/sridharkidambi/beelineProcessor'

        }
       }
      stage('download files from s3') {


         steps {
            sh 'aws configure set aws_access_key_id ${JENKINS_ACCESS_KEY_ID}'
            sh 'aws configure set aws_secret_access_key ${JENKINS_SECRET_ACCESS_KEY}'
            sh 'aws configure set default.region ${DEFAULT_REGION}'
            sh 'aws s3 sync s3://beelineprocess  files'

         }

      }

      stage('Process consolidation') {


         steps {

            echo '${params.NumberOfDays}'
            sh 'pip install -r requirement.txt'
            sh 'python ./excelprocessor.py "./files/${BaseFileName}" "./files/${NewFileName}" "./files/${AssignmentFileName}" "./files/" ${NumberOfDays} '

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