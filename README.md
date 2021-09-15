# FLiP-IoT
FLiP - IoT Examples with Go, Java, MiNiFi, Flink, Pulsar, StreamNative, JSON
FLiP = Apache FLink integrated with Apache Pulsar.   (And sometimes Apache NiFi and other Apache friends)


# Java Producer

https://github.com/streamnative/examples/tree/master/cloud/java

# Golang Producer

https://github.com/streamnative/examples/tree/master/cloud/go


# On NVIDIA Jetson I had JDK 11 and JDK 8.  OpenJDK on ARM64

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64

# Find and install java

update-alternatives --list java

/usr/lib/jvm/java-8-openjdk-arm64

# For Golang Client build

go mod tidy

# I am tailing a log

https://github.com/hpcloud/tail

go get github.com/hpcloud/tail/...
go mod tidy

# Run the Golang binary

./iot -serviceURL pulsar+ssl://istnace.streamnative.cloud:6651 \
       -privateKey instance-key.json\
       -audience urn:sn:pulsar:tenant:instance\
       -issuerUrl https://auth.streamnative.cloud\
       -clientId SOMECLIENTIDFORSTREAMNATIVE
       
       
# Run existing Jetson Python script

  #!/bin/bash

  DATE=$(date +"%Y-%m-%d_%H%M")
  python3 -W ignore /home/nvidia/nvme/minifi-jetson-xavier/demo.py --camera /dev/video0 --network googlenet /home/nvidia/nvme/images/$DATE.jpg  2>/dev/null

# Golang Build

go build -o iot iotproducer.go

# Run local

./iotlocal

# Local CLI Consumer

bin/pulsar-client consume "persistent://public/default/nvidia-sensor-partition-0" -s "nano2gbgo" -n 0


# Running sensors on NVIDIA Jetson Nano with environment sensor

python2 sensors.py

# Sensors

https://www.waveshare.com/environment-sensor-for-jetson-nano.htm

