# Non-Invasive-Ovulation-Predictor

### Motivation / Problem Statement
Many women track ovulation through the use of online apps or self tracking methods. However, these methods are error-prone and some are even invasive. This project will demonstrate the use of thermal cameras for tracking ovulation in a non-invasive way. The camera will be situated in a person’s bedroom aimed at the individual’s bed in order to monitor their body temperature during sleep. To maintain our non-invasive stance, the camera can be located as close as the edge of the bed or as far as the ceiling or wall of the room as long as we have a full body view of the sleeping individual.

### Hardware
 Seek Thermal Camera, Embedded Platform, Desktop App (Time Permitting)
 
### Design Goals
Our design goals are to implement thermal cameras to track the body temperature of someone sleeping. Based on collected data we will analyze and process relevant features. We will then develop a model for the user that allows them to be able to track ovulation based on temperature feedback during sleep.

### Deliverables
- We will determine the accuracy of thermal cameras in detecting change in temperature over varying distances. 
- Alongside distance, we will incorporate data and research based on the coverage of the sleeper, whether it be heavy/light clothing or blankets that may affect accurate thermal detection. 
- Finally we will use thermal data to see how long our model takes to accurately predict ovulation, if at all. If this is possible, we will project a timeline to see if this prediction is able to improve over time.

### System Block Diagrams

#### Software Block Diagram
https://lucid.app/lucidchart/262ba8cf-6c0f-488d-a46f-fd511e4fd590/edit?viewport_loc=60%2C-34%2C1707%2C779%2C0_0&invitationId=inv_3d2bec2d-08d7-41fe-a1dc-6a36ba7419f9
#### System Block Diagram

### Hardware Requirements
- Mobile: System can be setup in most envionrments and is easy to mount.
- Efficient: System is not power hungry and can go lengths beetween charging. (Is this correct?!)
- Thermal Camera: Camera works over a variety of distances. Camera is able to work in different sleeping positions.

### Software Requirements
- Thermal Camera: Be able to identify then filter bad data (like environmental noise or interference).
- Model: Model learns and trains with the specific user, and is able to gain accuracy over time.
- Connectivity: System is able to wirelessly transmit the prediction score to a front end GUI (This is an app if time permits)

### Team Member Responsibilities
- Brendan & Will: Building enclosure, setting up hardware, testing hardware, Wireless communication to front end GUI (App time permitting),
- John & Alina: Thermal Camera software, training of model for predictive score

### Project Timeline


### References
- Detection and prediction of ovulation from body temperature measured by an in-ear wearable
thermometer.
- FluSense: a contactless syndromic surveillance platform for influenza-like illness in hospital
waiting areas.
- Infrared thermography and behavioral biometrics associated with estrus indicators and ovulation
in estrus-synchronized dairy cows housed in tiestalls
