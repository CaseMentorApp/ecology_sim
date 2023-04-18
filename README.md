# ecology_sim
a dashboard that simulates ecological situations

an web app that presents 3 simulations.
all the matrial for each simulation is located in the folder with the corresponding names as png files.
the name of the images in animals and plants will be the names presented in the app and are also the name for the logical test for the right species in each simulation

in order to present the map image in the right way you have to use the image splitter which splits and image into 288 pieces and then move the images into the split image directory. the conditions for each square in the map are taken from the for refrence csv in each folder.
split image documentaion is in the link below:
https://pypi.org/project/split-image/

the web app starts with a login file, the login credentials are in the config.yaml file, in order to add cerdentials to the file you need to add the username info as seen now on the file in the format below
the exipry days is the number of days the login coockies are saved.
the password is the tricky part, in order to change or add a password you need to open the password hasher.py input the password you want and than paste the output you get in the password part of the config.yaml file(it will look diffrent since it is hashed but it will be the password you put it the input)
cookie:
  expiry_days: 30   
  key: random_signature_key
  name: random_cookie_name
credentials:
  usernames:
    Admin:
      email: random@gmail.com
      name: Admin
      password: $2b$12$/p3teKg7CxIG0I/6LM/T2ubUz5/F8H3sX9IItahR10qFdlcEmryj.
preauthorized:
  emails:
  - mail@gmail.com
  
