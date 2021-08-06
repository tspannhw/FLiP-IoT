export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64

java -jar target/IoTProducer-1.0-jar-with-dependencies.jar 
--serviceUrl pulsar+ssl://STREAMNATIVE.cloud:6651 
--audience urn:sn:pulsar:TENANT:INSTANCE 
--issuerUrl https://auth.streamnative.cloud 
--privateKey file:///home/nvidia/nvme/examples/cloud/java/INSTANCE-tspann.json 
--message "`tail -1 /home/nvidia/nvme/logs/demo1.log`"
