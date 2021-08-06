// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

package io.streamnative.examples.oauth2;

import com.beust.jcommander.JCommander;
import java.util.UUID;
import java.net.URL;
import org.apache.pulsar.client.api.Producer;
import org.apache.pulsar.client.api.ProducerBuilder;
import org.apache.pulsar.client.api.PulsarClient;
import org.apache.pulsar.client.api.MessageId;

import org.apache.pulsar.client.impl.auth.oauth2.AuthenticationFactoryOAuth2;

public class IoTProducer {
    public static void main(String[] args) throws Exception {
        JCommanderPulsar jct = new JCommanderPulsar();
        JCommander jCommander = new JCommander(jct, args);
        if (jct.help) {
            jCommander.usage();
            return;
        }

  // TODO pass as parameter
  String topic = "persistent://public/default/jetson-iot";

  // add logging, disable this 
	System.out.println("serv:" + jct.serviceUrl);
	System.out.println("issuer:"+ jct.issuerUrl);
	System.out.println("creds:" + jct.credentialsUrl);
	System.out.println("aud:" + jct.audience);
	System.out.println("msg:" + jct.message);

        PulsarClient client = PulsarClient.builder()
                .serviceUrl(jct.serviceUrl.toString())
                .authentication(
                        AuthenticationFactoryOAuth2.clientCredentials(new URL(jct.issuerUrl.toString()), new URL(jct.credentialsUrl.toString()), jct.audience.toString()))
                .build();

	UUID uuidKey = UUID.randomUUID();
	String pulsarKey = uuidKey.toString();
        String OS = System.getProperty("os.name").toLowerCase();

        ProducerBuilder<byte[]> producerBuilder = client.newProducer().topic(topic)
                .producerName("jetson");
        Producer<byte[]> producer = producerBuilder.create();

        String message = "" + jct.message;
        MessageId msgID = producer.newMessage().key(pulsarKey).value(message.getBytes())
		                  .property("device",OS).send();
        System.out.println("Publish " + "-" + message + " and message ID " + msgID);
	System.out.println("OS:" + OS + " Key:" + pulsarKey);
      
      // add more output metrics perhaps send to log
        producer.close();
        client.close();
	producer = null;
	client = null;
    }
}
