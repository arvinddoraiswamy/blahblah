##Defining all 14 AWS regions for use in every query in this script
##regions=( 'us-east-1' 'us-east-2' 'us-west-1' 'us-west-2' 'ca-central-1' 'eu-west-1' 'eu-central-1' 'eu-west-2' 'ap-northeast-1' 'ap-northeast-2' 'ap-southeast-1' 'ap-southeast-2' 'ap-south-1' 'sa-east-1')
#
##Choosing 1 region to use as a global region for global services
global_region=us-east-1
#
##Uncommented only during testing
regions=( 'us-east-1' 'us-west-2' ) 
#
outputdir='output'
rm -rf $outputdir
mkdir $outputdir

#Per Region Services
for region in "${regions[@]}"
do
    echo -e   "Testing per region services for region $region"
    mkdir -p $outputdir/$region
#    #CloudTrail
#    #    - Is cloud trail enabled across all regions?
#    #    - Is log-file-validation turned on?
#    #    - Are trails encrypted?
#    service=cloudtrail
#    echo -e   "\nCloudtrail configuration in region:'$region'..."  > $outputdir/$region/$service.txt
#    aws cloudtrail describe-trails --region $region --query 'trailList[*].{name:Name, log_file_validate:LogFileValidationEnabled, in_all_regions:IsMultiRegionTrail, KmsKeyId:KmsKeyId}' > $outputdir/$region/$service.txt
#
#    #CloudWatch
#    #    - Are alarms enabled for specific services that your functionality needs? For e.g If you depend on S3, have S3 related CloudWatch alarms.
#    service=cloudwatch
#    echo -e   "\nCloudwatch configuration in region:'$region'..."  > $outputdir/$region/$service.txt
#    aws cloudwatch describe-alarms --region $region --query 'MetricAlarms[*].{Service:Namespace, Metric:MetricName, Threshold:Threshold, Actions:AlarmActions}' > $outputdir/$region/$service.txt
#
#    #EC2
#    #   - Any instances with no EC2 keys attached? 
#    service=ec2
#    echo -e "\nEC2 configuration in region:'$region'..."  > $outputdir/$region/$service.txt
#    aws ec2 describe-instances --region $region --query 'Reservations[*].Instances[*].{EC2_Instance_Id:InstanceId, KeyPairName: KeyName, PublicIP:PublicIpAddress}'  >> $outputdir/$region/$service.txt
#    echo -e "\n***********Connect to the public IPs above and see if you get prompted for a password. It means SSH password authentication is enabled.**************"  >> $outputdir/$region/$service.txt
#    echo -e "--------" >> $outputdir/$region/$service.txt
#
#    #   - EC2 Security Groups not overly permissive
#    aws ec2 describe-security-groups --region $region --query 'SecurityGroups[*].{"GroupName":GroupName, "ipv4":IpPermissions[*].IpRanges[*].CidrIp, "ipv6":IpPermissions[*].Ipv6Ranges[*].CidrIp, "fromport":IpPermissions[*].FromPort, "toport":IpPermissions[*].ToPort}'  >> $outputdir/$region/$service.txt
#
#    echo -e "--------" >> $outputdir/$region/$service.txt
#     #   - EC2 Instance Termination Protection
#     for instanceid in `aws ec2 describe-instances --region $region --output text --query Reservations[*].Instances[*].InstanceId`
#     do
#        aws ec2 describe-instance-attribute --region $region --instance-id $instanceid --attribute disableApiTermination >> $outputdir/$region/$service.txt
#     done
#
#    #	- RDS List instances
#    #  - RDS backup configuration
#    #  - RDS data store encryption
#    #  - RDS not multi Availability Zone
#    #	- RDS security groups
#    #  - RDS Public DB Snapshots
#
#    service=rds
#    echo -e   "\nRDS List DB Instances\n"  >> $outputdir/$region/$service.txt
#    aws rds describe-db-instances --query 'DBInstanceIdentifier' --output text --region $region  >> $outputdir/$region/$service.txt
#
#    echo -e   "\nRDS Backups not enabled in region, encrypted or in a multiAZ in $region\n"  >> $outputdir/$region/$service.txt
#    aws rds describe-db-instances --query 'DBInstances[?BackupRetentionPeriod == `0`].[DBInstanceArn, StorageEncrypted, MultiAZ]' --output text --region $region  >> $outputdir/$region/$service.txt
#
#    echo -e   "\nRDS Security Groups, if they're configured and not in a VPC\n"  >> $outputdir/$region/$service.txt
#    aws rds describe-db-security-groups --region $region  >> $outputdir/$region/$service.txt
#
#    echo -e   "\nRDS Public DB Snapshots\n"  >> $outputdir/$region/$service.txt
#    aws rds describe-db-snapshots --region $region --snapshot-type manual --query "DBSnapshots[*].{id:DBSnapshotIdentifier, arn:DBSnapshotArn, type:SnapshotType}"  >> $outputdir/$region/$service.txt
#    aws rds describe-db-snapshots --region $region --snapshot-type automated --query "DBSnapshots[*].{id:DBSnapshotIdentifier, arn:DBSnapshotArn, type:SnapshotType}"  >> $outputdir/$region/$service.txt
#
#    #	- SQS Queue Permissions
#    service=sqs
#    echo -e   "\nSQS queue permissions in $region\n" >  $outputdir/$region/$service.txt
#    for queue in `aws sqs list-queues --query 'QueueUrls[*]' --region $region --output text|grep -iv none`
#    do
#        aws sqs get-queue-attributes --queue-url $queue --attribute-names QueueArn Policy --region $region  > $outputdir/$region/$service.txt
#    done
#
#    #	- VPC NACLs
#    service=vpc
#    echo -e   "\nVPC Network Access Control Lists in $region\n"  >> $outputdir/$region/$service.txt
#    aws ec2 describe-network-acls --region $region --query 'NetworkAcls[*].[VpcId, Associations[*].[SubnetId, NetworkAclId], Entries[*].[CidrBlock, RuleAction, Egress]]'  >> $outputdir/$region/$service.txt
#
#    #   - CloudFormation Stack Policy and Termination Protection
#    service=cloudformation
#    echo -e   "\nCloudFormation stack policy in $region\n"  >> $outputdir/$region/$service.txt
#    for policy in `aws cloudformation list-stacks --region $region --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query 'StackSummaries[*].StackId' --output text`
#    do
#        aws cloudformation get-stack-policy --stack-name $policy --region $region --output text  >> $outputdir/$region/$service.txt
#    done
#
#    echo -e   "\nCloudFormation stack termination protection in $region\n"  >> $outputdir/$region/$service.txt
##   *********This does not appear to work properly and nothing returns*****
#    for stackname in `aws cloudformation list-stacks --region $region --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query 'StackSummaries[*].StackName' --output text`
#    do
#        aws cloudformation describe-stacks --region $region --stack-name $stackname --query 'Stacks[*].EnableTerminationProtection' --output text >> $outputdir/$region/$service.txt
#    done
#
    #   - ELBv2 Application Load Balancer attributes
    service=elbv2
    echo -e   "\nELBv2 Load Balancers in $region\n"  >> $outputdir/$region/$service.txt
    for loadbalancer in `aws elbv2 describe-load-balancers --region $region --query "LoadBalancers[*].LoadBalancerArn" --output text`
    do
        echo -e "\nNetwork/Application Load balancer Deletion protection for $loadbalancer in $region\n"  >> $outputdir/$region/$service.txt
        aws elbv2 describe-load-balancer-attributes --region $region --load-balancer-arn $loadbalancer  >> $outputdir/$region/$service.txt
        echo -e "\nOlder insecure load balancer SSL policy\n" >> $outputdir/$region/$service.txt
        aws elbv2 describe-listeners --region $region --load-balancer-arn $loadbalancer --query 'Listeners[*].{loadbalancerarn:LoadBalancerArn, sslpolicy:SslPolicy}' --output text >> $outputdir/$region/$service.txt
    done
#
#    #   - SNS Topic permissions
#    service=sns
#    echo -e   "\nSNS Topics in $region\n"  >> $outputdir/$region/$service.txt
#    for topic in `aws sns list-topics --region $region --query "Topics[*].TopicArn" --output text`
#    do
#        echo -e   "\nSNS Topic permissions for $topic in $region\n"  >> $outputdir/$region/$service.txt
#        aws sns get-topic-attributes --topic-arn $topic --region $region --query "Attributes.Policy" --output text  >> $outputdir/$region/$service.txt
#    done
#
#    #   - SES Identity Permissions
#    service=ses
#    echo -e   "\nSES Identity Permissions in $region\n"  >> $outputdir/$region/$service.txt
#    for identity in `aws ses list-identities --region $region --query "Identities" --output text`
#    do
#        for policyname in `aws ses list-identity-policies --identity $identity --region $region --output text --query "PolicyNames"`
#        do
#        aws ses get-identity-policies --identity $identity --policy-names $policyname --region $region --output text --query "Policies"  >> $outputdir/$region/$service.txt
#        done
#    done
#
#    #   - RedShift Cluster security
#    service=redshift
#    echo -e   "\nRedshift Cluster security\n"  >> $outputdir/$region/$service.txt
#    aws redshift describe-clusters --region $region --query "Clusters[*].{"id":ClusterIdentifier, "public":PubliclyAccessible, "versionupgrade":AllowVersionUpgrade, "encrypted":Encrypted}"  >> $outputdir/$region/$service.txt 2>&1
#
#    for clusterid in `aws redshift describe-clusters --region $region --query "Clusters[*].ClusterIdentifier" --output text`
#    do
#    aws redshift describe-logging-status --region $region --cluster-identifier $clusterid  >> $outputdir/$region/$service.txt 2>&1
#    done
#
#    for pg in `aws redshift describe-cluster-parameter-groups --region $region --query "ParameterGroups[*].ParameterGroupName" --output text`
#    do
#    aws redshift describe-cluster-parameters --region $region --parameter-group-name "$pg" --query "Parameters[?ParameterName == 'require_ssl'].[Description, ParameterName, ParameterValue]"  >> $outputdir/$region/$service.txt 2>&1
#    done
#
#    aws redshift describe-cluster-security-groups --region $region --query "ClusterSecurityGroups[*].IpRanges" --output text  >> $outputdir/$region/$service.txt 2>&1
#
#    #   - ACM Expired certificates
#    service=acm
#    echo -e "\nACM Expired Certificates\n"  >> $outputdir/$region/$service.txt
#    aws acm list-certificates --region $region --certificate-statuses EXPIRED  >> $outputdir/$region/$service.txt
#
#    #   - WAF Regional List ACLs
#    service=waf
#    echo -e   "\nWAF ACLs per region\n"  >> $outputdir/$region/$service.txt
#    aws waf-regional list-web-acls --region $region  >> $outputdir/$region/$service.txt

    #   - API Gateway Logging
#    service=apigateway
#    echo -e "\nAPI Gateway Stage wise API logging\n" >> $outputdir/$region/$service.txt
#    for api in `aws apigateway get-rest-apis --region $region --output text --query 'items[*].id'`
#    do
#        echo -e `aws apigateway get-stages --rest-api-id $api --query "item[*].[stageName, methodSettings]" --region $region`
#    done

#   #   - AutoScaling
#   #NO TESTS as of now. Will revisit later

#   #   - EBS Volume & Snapshot Encryption
#    service=ec2_ebs
#    echo -e "\nEBS Volume configuration in region:'$region'..."  >> $outputdir/$region/$service.txt
#    aws ec2 describe-volumes --region $region --query "Volumes[*].{volumeid:VolumeId,encrypted:Encrypted}" >> $outputdir/$region/$service.txt
#    echo -e "\nEBS Snapshot configuration in region:'$region'..."  >> $outputdir/$region/$service.txt
#    for snapshotid in `aws ec2 describe-volumes --region $region --query "Volumes[*].SnapshotId" --output text`
#    do
#        aws ec2 describe-snapshots --snapshot-id $snapshotid --region $region --query "Snapshots[*].{snapshotid:SnapshotId, encrypted:Encrypted}" >> $outputdir/$region/$service.txt
#    done

#   #   - EFS FileSystem Encryption
#    service=efs
#    echo -e "\nEFS Filesystem configuration in region:'$region'..."  >> $outputdir/$region/$service.txt
#    for filesystemid in `aws efs describe-file-systems --region us-east-1 --query 'FileSystems[*].FileSystemId' --output text`
#    do
#        aws efs describe-file-systems --region us-east-1 --file-system-id $filesystemid --query 'FileSystems[*].{filesystemid:FileSystemId, encrypted:Encrypted}' >> $outputdir/$region/$service.txt
#    done
#   #   - Elastic Beanstalk Logging
#     service=elasticbeanstalk
#     echo -e "\nElastic Beanstalk in region :'$region'..."  >> $outputdir/$region/$service.txt
#     echo -e >> $outputdir/$region/$service.txt
#     environments=`aws elasticbeanstalk describe-environments --region $region --output text --query 'Environments[*].EnvironmentName'`
#     for env in $environments
#     do
#        for appname in `aws elasticbeanstalk describe-environments --region $region --environment-names $env --query 'Environments[*].ApplicationName' --output text`
#            do
#                echo "Environment name - $env" >> $outputdir/$region/$service.txt
#                echo "Application name - $appname" >> $outputdir/$region/$service.txt
#                aws elasticbeanstalk describe-configuration-settings --region $region --environment-name $env --application-name $appname --query 'ConfigurationSettings[*].OptionSettings[?OptionName==`LogPublicationControl` || OptionName==`StreamLogs`] | []' >> $outputdir/$region/$service.txt
#            done
#     done

   #   - Elasticache Database encryption
     service=elasticache
     echo -e "\nElasticache in region :'$region'..."  >> $outputdir/$region/$service.txt
     echo -e >> $outputdir/$region/$service.txt
     for cluster in `aws elasticache describe-cache-clusters --region $region --query "CacheClusters[?(Engine=='redis') && (EngineVersion=='3.2.6')].ReplicationGroupId" --output text`
     do
        aws elasticache describe-replication-groups --region $region --replication-group-id $cluster --query 'ReplicationGroups[*].{id:ReplicationGroupId, encryptionatrest:AtRestEncryptionEnabled, encryptionintransit:TransitEncryptionEnabled}' >> $outputdir/$region/$service.txt
     done

#   #   - Elastic Search
    service=elasticsearch
    echo -e "\nAccess to ES clusters in region via over-permissive polices: $region\n" >> $outputdir/$region/$service.txt
    echo -e >> $outputdir/$region/$service.txt
    for domainname in `aws es list-domain-names --region $region --output text --query 'DomainNames[*].DomainName'`
    do
        aws es describe-elasticsearch-domain --domain-name $domainname --region $region --query 'DomainStatus.{accesspolicies:AccessPolicies, endpoint:Endpoint, encryptionatrest:EncryptionAtRestOptions}' >> $outputdir/$region/$service.txt
    done
done

###Global Configuration Services
##
##echo -e   "\nTesting services that are region independent\n"
###IAM
##
###   - List access keys created more than 180 days ago.
#
#service=iam
#echo -e   "\nTesting $service\n"
#d1=$(date +%Y-%m-%d -d "180 days ago")
#for user in `aws iam list-users --query 'Users[*].UserName' --region $global_region --output text`
#do
#    echo -e   "\nIAM Access Keys > 180 days old for user:'$user'..."   >> $outputdir/$service.txt
#    aws iam list-access-keys --user-name $user --query "AccessKeyMetadata[?CreateDate <= '$d1'].[UserName, CreateDate, AccessKeyId]" --region $global_region >> $outputdir/$service.txt
#done
#
##   - List permissions given by IAM policies and the users attached to it
#
#for policy in `aws iam list-policies --only-attached --query 'Policies[*].Arn' --region $global_region --output text`
#do
#    echo -e   "Policy Document $policy" >> $outputdir/$service.txt
#    echo -e   "-----------------" >> $outputdir/$service.txt
#    aws iam get-policy-version --policy-arn $policy --version-id `aws iam list-policy-versions --policy-arn $policy --query "Versions[?IsDefaultVersion].VersionId" --region $global_region --output text` --region $global_region >> $outputdir/$service.txt
#
#    echo -e   "Users/Roles attached to the policy $policy" >> $outputdir/$service.txt
#    echo -e   "-----------------" >> $outputdir/$service.txt
#    aws iam list-entities-for-policy --policy-arn $policy --region $global_region >> $outputdir/$service.txt
#    echo -e   "\n\n" >> $outputdir/$service.txt
#done
#
##   - Study Inline policies per user
#for user in `aws iam list-users --query 'Users[*].UserName' --region $global_region --output text`
#do
#    for policy in `aws iam list-user-policies --region $global_region --output text --user-name $user --query "PolicyNames"`
#    do
#        echo -e   "\nInline policies for user $user\n" >> $outputdir/$service.txt
#        aws iam get-user-policy --region $global_region --user-name $user --policy-name $policy >> $outputdir/$service.txt
#    done
#done
#
##   - Check account password policy and see if any users who login via password exist
#echo -e   "Account Password Policy" >> $outputdir/$service.txt
#aws iam get-account-password-policy --region $global_region >> $outputdir/$service.txt
#
##   - Users who have passwords
#echo -e   "List of users who have passwords and have logged in at least once, sometime" >> $outputdir/$service.txt
#aws iam get-credential-report --region $global_region --query "Content" --output text|base64 --decode|cut -d ',' -f1,4,5|grep -i 'true'|cut -d',' -f1 >> $outputdir/$service.txt
#
##   - S3 Bucket Security
#    #	- S3 Bucket Policies
#    #	- S3 CORS Policies
#    #	- S3 Logging Policies
#    #	- S3 Versioning policies
#service=s3
#echo -e   "Testing $service"
#for bucket in `aws s3api list-buckets --query "Buckets[].Name" --output text --region $global_region`
#do
#    echo -e   "\nTesting bucket $bucket\n" >> $outputdir/$service.txt 2>&1
#    echo -e   "S3 bucket policies for $bucket" >> $outputdir/$service.txt
#    aws s3api get-bucket-acl --bucket $bucket --region $global_region >> $outputdir/$service.txt 2>&1
#    echo -e   >> $outputdir/$service.txt
#
#    echo -e   "S3 CORS Policies for bucket $bucket" >> $outputdir/$service.txt
#    aws s3api get-bucket-cors --bucket $bucket --region $global_region >> $outputdir/$service.txt 2>&1
#    echo -e   >> $outputdir/$service.txt
#
#    echo -e   "S3 Logging for bucket $bucket" >> $outputdir/$service.txt
#    aws s3api get-bucket-logging --bucket $bucket --region $global_region >> $outputdir/$service.txt
#    echo -e   >> $outputdir/$service.txt
#
#    echo -e   "S3 Versioning for bucket $bucket" >> $outputdir/$service.txt
#    echo -e   "MFA Delete for bucket $bucket" >> $outputdir/$service.txt
#
#    #If output is blank, it means versioning & MFA delete is not enabled
#    aws s3api get-bucket-versioning --bucket $bucket --region $global_region --query "[Status,MFADelete]" >> $outputdir/$service.txt
#
#    echo -e   "Publicly accessible bucket for bucket $bucket" >> $outputdir/$service.txt
#done
#
##   - CloudFront security
#    #   - Integration with WAF
#    #   - ACL Logging
#    #   - Origin Access Identity
#    #   - Origin Insecure SSL protocols
#    #   - Cloudfront security policy
#    #   - Unencrypted AWS Cloudfront traffic
#service=cloudfront
#echo -e  "Testing $service"
#for distribution in `aws cloudfront list-distributions --query 'DistributionList.Items[*].Id' --output text --region $global_region`
#do
#    echo -e   "\nTesting distribution $distribution\n"  >> $outputdir/$service.txt
#    echo -e   "WAF integration\n" >> $outputdir/$service.txt
#    aws cloudfront get-distribution --id $distribution --query 'Distribution.DistributionConfig.WebACLId' --region $global_region >> $outputdir/$service.txt
#
#    echo -e  "\nAccess logs\n" >> $outputdir/$service.txt
#    aws cloudfront get-distribution --id $distribution --query 'Distribution.DistributionConfig.Logging.Enabled' --region $global_region >> $outputdir/$service.txt
#
#    echo -e  "\nOrigin Access Identity\n"  >> $outputdir/$service.txt
#    aws cloudfront get-distribution-config --id $distribution --query 'DistributionConfig.Origins.Items[*].S3OriginConfig.OriginAccessIdentity' --region $global_region  >> $outputdir/$service.txt
#
#    echo -e  "\nTLS protocol support\n" >> $outputdir/$service.txt
#    aws cloudfront get-distribution --id $distribution --query 'Distribution.DistributionConfig.Origins.Items[*].CustomOriginConfig.OriginSslProtocols.Items' --region $global_region  >> $outputdir/$service.txt
#
#    echo -e  "\nTLS preferred protocol and cipher\n"  >> $outputdir/$service.txt
#    aws cloudfront get-distribution --id $distribution --query 'Distribution.DistributionConfig.ViewerCertificate.MinimumProtocolVersion' --region $global_region >> $outputdir/$service.txt
#
#    echo -e  "\nEncrypted traffic between CF and destination\n" >> $outputdir/$service.txt
#    aws cloudfront get-distribution --id $distribution --query 'Distribution.DistributionConfig.Origins.Items[*].CustomOriginConfig.OriginProtocolPolicy' --region $global_region >> $outputdir/$service.txt
#done
#
##   - WAF Security
##    #   - Presence of some Web ACLs
#service=waf
#echo -e  "Testing $service" >> $outputdir/$service.txt
#aws waf list-web-acls --region $global_region >> $outputdir/$service.txt
