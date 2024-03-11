# Checkpoint 1 - Domain & Problem Analysis

*Authors' note: This report shares fragments with [EPANET optimization project](https://github.com/michwoj01/Computation-Intelligence---EPANET-optimization/wiki/Stage-1:-Analysis-of-the-problem-and-the-field) checkpoint 1 wiki page.*

_____

## Domain Analysis

Drinking water distribution systems connect water treatment plants or water sources (in the absence of treatment) to customers via a network of pipes, storage facilities, valves, and pumps. 
In addition to providing water for domestic use, distribution systems may supply water for fire protection, agricultural, and commercial uses.

Public water systems (PWSs) are responsible for operating and maintaining their distribution systems, which extend from the designated entry point to the distribution system (EPTDS) 
– typically the source or water treatment plant - up to the service connection, after which the piping is the property owner’s responsibility.

Distribution systems represent the vast majority of the physical infrastructure for water systems and serve as the final barrier against contamination. 
These systems must be operated and maintained to reduce the risk of contamination from external sources or internal sources such as 
microbial growth or corrosion within the system.


### State of polish waterworks
According to [Polish National Control Panel's (NIK) report](https://www.nik.gov.pl/plik/id,17663,v,artykul_16798.pdf) in 2015 Polish PWSs consisted of 8502 waterworks and 
provided water for around 36 mln people (92% of Poland's population).\
More importantly we have to consider the other message the report includes. In most of the Polish cities
nearly 50% of the waterworks systems are 25-50 years old! Furthermore, another 45% is over 20 years old! It's not the case for all cities, but we have to bear in mind
that on average around 75% of the cities' waterworks is consequentially old, older than the authors of the project to be exact. As usual the rural areas do not fair better in that metric.

<p align="center">
    <img src="images/age_of_rural_waterworks_2020.png" height="550">
</p>

Thereupon it shouldn't come as a surprise that the technical state of polish PWSs is poor. And such state is a result of years and years of the underfunding of the conservation and modernization
of the network as well as insufficient investment in the replacement of the eldest parts of the infrastructure. What is more, if the current rate of replacement is 
maintained it would take approximately 100 years to fully replace the whole system. It is debatable if we can even call such process an upgrade at all...\
In the last 20 years most of the funding for the PWSs came from the UE. In 2015 the whole budget reached 1.8 billion zł. If all of that wasn't bad enough, NIK's investigation in the following years suggests that there is a general lack of information regarding system's current state
and plans for its modernization and development are poorly built, researched and implemented.


_____

## Leaks problem analysis

Water loss from distribution system leaks and main breaks can result in lost revenue for the water system, wasted resources, and water quality concerns. 
Reducing water loss involves identifying and repairing breaches in the distribution system which, in addition to being sources of lost water, represent potential entry points for contamination to the system.


### Scale of the problem in Poland with examples

Different sources present different amount of water lost in the waterworks. In the aforementioned NIK's report in 2016 **the average loss in the PWS was 15.2%**, with the lowest rate being 4.15% achieved in Dębica, and the highest equal to 21.2% in Zduńska Wola.
 It's important to know that the investigation only included 12 cities across the country.

<p align="center">
    <img src="images/water_distribution_in_cities_2014_2016.png" height="400">
</p>

However, that's the case in the cities. The situation in the rural areas is even worse. In 2022 the [article from Polish newspaper - Dziennik Gazeta Prawna](https://serwisy.gazetaprawna.pl/samorzad/artykuly/8526291,nik-straty-wody-raport.html) claimed that
a [newer NIK's investigation](https://www.nik.gov.pl/plik/id,26438,vp,29229.pdf) from 2020-2021 conducted in several voivodeships found out that in over a half of the controlled communes **the losses surpassed 30%**, in 45% of the cases the loses were estimated at 45% of the water that has entered the systems, and
in 6 cases, the losses contributed to over 60%!

This state of affairs results in massive economical losses estimated at 21 mln zł, just from that one 2020-2021 report. Moreover, we cannot forget about the environmental consequences of such losses,
as Poland is considered a country with scarce water resources (24th in the UE in the renewable fresh water resources per citizen).

While the main reason for the losses is a bad technical state of the pipelines, not everything is as straightforward as it seems. When asked about the actions taken to prevent water losses, the local municipalities often answered that
with the current prices of water and received funding the costs of the waterworks fixes or replacements would massively outweigh the funds and would not repay for years to come.\
In 2016 NIK report, it was mentioned that out of the 12 investigated cities in 4 of them the local authorities did not have any data
regarding the loss of water in the waterworks. The lack of information was then used as another argument for not taking any action against the losses.

It's also important to consider that not all losses are caused by the bad technical state of the pipes. In rural areas some part of them is caused by theft as farmers illegally water their fields with the "liberated" water. 

For rural areas nearly all of those points were raised in [another NIK report](https://www.nik.gov.pl/aktualnosci/zmarnowane-miliardy-litrow-wody-na-wsiach.html) from 2022.

In conclusion:
* While different for each city and commune, the average water losses reach around 15% in the cities, and around 45% in rural areas.
* The main cause of the leaks is a bad technical state of the waterworks.
* The lack of data, planning and misplaced resources make it hard for municipalities to modernize or replace failing parts of the network. While not the only ones responsible, the local authorities fall victim to their own policies.
* Rural areas are more prone to the theft, which contributes to the higher loss in the aforementioned areas.
* The economical and environmental repercussions of such state of the PWSs are much more grave than most citizens think.

### Classes of leak detection models

Through the observation of the literature and the applied works in leak detection, two main categories of leak detection systems can be identified. The categories are static (or stationary) leak detection and dynamic (or mobile) leak detection. Although each class on its own is capable of identifying, locating, and pinpointing leaks, it is not uncommon to utilize a combination of both classes. The two classes of leak detection system can be
defined as follows:
* Static leak detection systems: are systems that rely on sensors and data collectors that are placed within the water network and on valves and are capable of transmitting periodical data to the network management office. This data can be used to identify, localize, and pinpoint leaks.
* Dynamic leak detection systems: are systems that rely on moving leak detection devices to suspected leakage area to perform an investigation. Therefore, they rely initially on suspicion of an existing leak. Another approach is performing regular surveys around cities to identify leaks as soon as possible. Those systems can confirm the existence of leaks and immediately localize and pinpoint them. 

The main distinction between the two classes is that static leak detection systems can inform the water network management of the existence of a leak almost immediately, whereas dynamic leak detection systems are required to have information of a leak possibility so that they can be mobilized for investigation. On the other hand, dynamic leak detection systems can pinpoint the exact location of a leak almost immediately under ideal operating conditions, whereas static leak detection systems will provide a location within a certain area, and they are also more prone to false alarms. It is not uncommon to use a static leak detection system to detect leaks and a dynamic leak detection system to pinpoint them, but that is not expected to be the most affordable route. The two classes encompass a wide variety of technologies to provide an accurate leak detection system, but the technologies are not limited to one class. For example, acoustic technologies, specifically noise loggers, can be dynamic and moved from one location to the other periodically to detect leaks, or they can be left in the network.

### Leak detection technologies overview

Multiple technologies have been developed throughout the years to help identify and locate leaks within water networks.
 
![Distribution of technologies](https://github.com/michwoj01/Computational-Intelligence---EPANET-optimization/blob/main/resources/models.PNG)

1. Listening devices

Both electrical and mechanical geophones are used to listen to buried water pipelines from the surface. These devices are accurate and highly sensitive that they can detect the exact location of the leak, and also cheap to purchase and easy to set up. Its accuracy depends highly on the proficiency and the experience of the operator, and it also might fail to detect some leak classes. Furthermore, the exact location of the pipeline to be assessed must be marked so that the operator would know where to put the device. The examination renders the area above the pipe unusable in case it is a street or highly utilized area. Similar to Geophones, Hydrophones try to listen to leaks by sometimes being placed in the system and rarely on the surface of the ground. Hydrophones can be more accurate than geophones in detecting leaks, but they require more training, and they are approximately seven times more
expensive than geophones. To detect a leak, they rely on the high-frequency acoustic signals sent by the release of pressurized fluids, to detect leak existence and locations. Sound frequencies are then amplified and filtered at 1 kHz using a preamplifier to remove high frequency noises that are not related to the network. By measuring the time delay between two detection instants between two given listeners the leak can be pinpointed by relating propagation speed within the medium with time and distance.

2. Leak noise loggers

Leak Noise loggers are placed in utility holes without any trenching or drilling; they can be used as a permanent, semi-permanent monitoring, or leak surveying technique. Noise Loggers operate by implementing sophisticated algorithms to identify the sound emitted by normal operations compared to that of the leak (immediate identification). Also, this technology is automatic, thus eliminating human error. Noise loggers also have low maintenance and battery replacement cost for long-term use. This technology has a very high initial cost for a real-time monitoring system, and it does not identify the exact leak location without the use of correlators. A logger system is usually composed of a set of loggers that are placed throughout the network, a communication base that delivers collected data, and an analysis base that can be a desktop computer or a cloud engine using big data platforms. Additionally, this system is utilized in highly pressurized water networks, which allow the extended propagation of leak signal. Furthermore, multiple loggers may operate at the same time to provide multiple detections for more accurate results. On the other hand, such systems have a room for improvement in correlation accuracy by means of self-learning algorithms or collective thinking algorithms, which allow the computational end of the system to keep improving constantly with new data.

3. Tracer gas

Tracer gasses is a leak detection technique that utilizes pressurizing nontoxic and insoluble gasses into leaks, these gasses contain ammonia, halogens, and helium, where helium is the most sensitive. Given that the utilized gasses are lighter than air they will tend to go out through leaks and then seep out through the soil or pavements. Later on, these gasses are traced and detected using a man operated detector to identify the
locations of leaks through detecting the seepage of tracer gasses. The gas injection approach is reliable in all types of materials, as it is not material type dependent. Additionally, tracer gases can detect leaks in pipelines that range from 75 mm to 1000 mm in diameter. Tracer gases are not conventionally used in larger pipelines due to the great expense associated with pumping a substantial amount of gas into the system. The method relies on knowing the flow of the water and blocking the gas from finding easier routes to exit the system. Blocking other routes is done by closing branches and cutting off the suspected leak area; this may cause interruption to the water distribution service. Furthermore, the gas may exit the ground from a different location than that of the leak; this is common in buried pipelines.

4. Wireless micro-electro-mechanical systems (MEMS)

Micro-Electro-Mechanical Systems are microfabricated mechanical and electromechanical devices and structures. MEMS are usually composed of four main
elements:
* Micro-Sensors
* Micro-Actuators
* Micro-Electronics
* Micro-Structures.

Multiple types of MEMS were used in leak detection of water mains mainly accelerometers, acoustic, and thermal. MEMS technology provides continuous water network monitoring for any leaks from the moment they are placed. MEMS have proven to be cost-effective tools when it comes to the detection of leaks with their low cost and high sensitivity to signal anomalies. On the other hand, MEMS are viable when used in metallic pipelines, whereas other material types require further research due to the material-induced attenuation of high-frequency signals. Additionally, the application of MEMS is still mostly theoretical and requires further research. Furthermore, MEMS needs further testing on long pipes. As in loggers, the field of MEMS requires software and signal analysis improvements to become more viable as a realistic solution for leak detection.

5. Data analysis based methods

In recent years, novel approaches have been developed that can be integrated with existing technologies to improve leak detection accuracy on all levels. Those approaches rely on have data analysis and range from statistical approaches to artificialintelligence based approaches. 

One of the most common methods is **regression analysis**. Regression analysis relies on having a sizable collection of data points that represent multiple aspects of a selected study. For example, in the case of leak detection using noise loggers, the factors can include the highest and lowest amplitude of the signal, the incremental distance between two sensors, and the frequency of the collected signals. Regression analysis then tries to determine an equation that best fits the collected set of data points. After model development, the model is checked for statistical soundness using a series of statistical tests. Regression analysis is having a lot of success as an emerging approach in leak detection with pinpointing accuracies reaching 93%. On the other hand, a developed model by regression analysis is situational, i.e. it can not be used for different pipelines or networks as they may have different operating conditions than the conditions where the model was developed. Regression models can be improved by integrating them with artificial intelligence, such that the model can be constantly improved with new data. Additionally, current regression models may acquire further accuracy by considering new characteristics of water networks such as pipeline material, soil type, pipeline age, and water pressure. 

Another popular method is **artificial neural networks (ANN)**. ANN helps compensate for the incompleteness or randomness of collected data. The approach mimics the human cerebral network of neurons in operation. Their uses vary from leak detection in water networks to condition assessment. ANN is a directed learning approach, in other words, it relies on previously collected high-quality data to develop a baseline. The data is placed in an input layer and then analyzed in at least one hidden layer. Finally, the desired outputs are placed in a single output layer. ANN does not provide an equation as in regression analysis as its approach relies on black-box-like algorithms, yet it may provide better results in the field of leak detection than that of regression analysis.

Multiple other techniques are being utilized as well for leak identification and detection. Such techniques include **Naïve Bayes algorithm (NB)**, **Decision Trees (DTs)**, and **Support Vector Machines (SVMs)**. The aforementioned techniques have presented great success in distinguishing leaks from other noises within the water network. Additionally, when the aforementioned techniques are coupled with a collective thinking code, their accuracy may reach 100%.
_____

## Short description of EPANET system

EPANET is a software application for understanding the movement and fate of drinking water constituents within a drinking water distribution system. It can be used to design and size new water infrastructure, retrofit existing aging infrastructure, optimize operations of tanks and pumps, reduce energy usage, investigate water quality problems, and prepare for emergencies.

What are its capabilities?:

* Ability to use pressure dependent demands in hydraulic analyses.
* System operation based on both simple tank level or timer controls and on complex rule-based controls.
* No limit on the size of the network that can be analyzed.
* Computes friction headloss using the Hazen-Williams, Darcy-Weisbach, or Chezy-Manning formulas.
* Includes minor head losses for bends, fittings, etc.
* Models constant or variable speed pumps.
* Computes pumping energy and cost.
* Models various types of valves, including shutoff, check, pressure regulating, and flow control.
* Allows storage tanks to have any shape (i.e., diameter can vary with height).
* Considers multiple demand categories at nodes, each with its own pattern of time variation.
* Models pressure-dependent flow issuing from emitters (sprinkler heads).
* Provides robust results for hydraulic convergence and low/zero flow conditions.
