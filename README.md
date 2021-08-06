# FLiP-IoT
FLiP - IoT Examples with Go, Java, MiNiFi, Flink, Pulsar, StreamNative, JSON


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
       
       
 
