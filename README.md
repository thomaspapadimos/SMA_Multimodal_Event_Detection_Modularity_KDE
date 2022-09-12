# Code for Real-time Alert Framework for Fire Incidents Using Multimodal Event Detection on Social Media Streams
This is the code from the paper published in Iscram 2022 https://zenodo.org/record/6414022#.Yx79l-xBw-Q



## Abstract

The overall architecture of our framework is illustrated in below Figure. First, we collect the tweets that will be used in
order to detect events. To retrieve them we have developed the Twitter Crawler that calls the Twitter Streaming API.
When a tweet matches the predefined search criteria, it is stored in a MongoDB database named “Tweets”. The
Event Detection module, running in a time interval that can be set, reads the tweets that have been stored in the
database and applies the proposed event detection methodology. When the occurrence of an event is identified,
the timestamp and the group of tweets it comprises are inserted in a MongoDB database named “Events”. When
the Event Detection module concludes, the Event Insights module is triggered and for each event the top ten most
mentioned keywords are extracted and stored, in order to provide the user with more details, and a corresponding
alert is generated

![Architect](https://github.com/thomaspapadimos/SMA_Multimodal_Event_Detection_Modularity_KDE/blob/master/images/architecture.png)

## Event detection

The proposed event detection methodology considers the fusion of two modalities: the first one refers to Kernel Density
Estimation (Efron et al. 2014) and the second one to Community Detection (De Meo et al. 2011).

![Architect](https://github.com/thomaspapadimos/SMA_Multimodal_Event_Detection_Modularity_KDE/blob/master/images/event_detection_methodology.jpg)



License
=======
  Copyright 2022 Thomas Papadimos

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
