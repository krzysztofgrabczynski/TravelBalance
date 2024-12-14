
# <p align=center> <a name="top">TravelBalance</a></p>

<p align=center><strong>Official website: <i>https://www.travelbalance.pl</i></strong></p>


## Short overview
**TravelBalance** is a mobile application for iOS and Android designed to help you manage your expenses while traveling. It allows users to easily create trips to any destination, add expenses in any currency, and seamlessly display all statistics, converting them into a chosen base currency. Our goal is to provide a practical solution for managing travel finances and helping travelers stay organized and stress-free.

This app was created by a team of two passionate developers and avid travelers:
- the mobile application frontend was created by https://github.com/BartlomiejGajdur
- the backend and <i><a href="https://www.travelbalance.pl">official website</a></i> were implemented by me

<br>

## Preview
<p align="center">
  <img src="https://github.com/user-attachments/assets/d15721d4-e8ac-4949-abbc-9983c25eb278" width="253" height="549"/>
  <img src="https://github.com/user-attachments/assets/03a2f777-bb82-47bf-9593-fac2d3ea3266" width="253" height="549"/>
  <img src="https://github.com/user-attachments/assets/d01f9a58-831f-4ec1-a10a-806d7b1c0151" width="253" height="549"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/bd70bd8a-ea00-41ff-8281-1604a46d8e36" width="253" height="549"/>
  <img src="https://github.com/user-attachments/assets/52b35338-129c-4b35-b3fa-8f7e0a062d0e" width="253" height="549"/>
  <img src="https://github.com/user-attachments/assets/c229c7c5-473e-4784-921f-6abf1b306eb3" width="253" height="549"/>
</p>

## Description
TravelBalance is a comprehensive mobile application designed for managing your travel expenses, available for both iOS and Android platforms. It provides features like adding trips, where you can choose a photo from a default images and optionally choose the countries you're visiting. Within each trip, you can log expenses in any currency, and the app will automatically convert them into your selected base currency (you can set base currency in main settings of the application). The app generates detailed visual statistics, including graph showing how much you've spent on different categories during each trip. On the main screen, you can view overall statistics, including the number of trips you've taken, the countries you've visited, and your total spending in your base currency. Additionally, TravelBalance offers a Pro version, which removes advertisements and provides an enhanced, ad-free experience.

The design of the application was created using Figma, ensuring a user-friendly and visually appealing experience. The frontend was developed by https://github.com/BartlomiejGajdur using Flutter, providing a smooth and responsive interface across both iOS and Android devices. The backend was built by me using the Django Rest Framework, ensuring secure and efficient handling of data. I also developed the <i><a href="https://www.travelbalance.pl">official website</a></i> for the app using HTML, CSS, JavaScript and took care of the server set up on a virtual machine. 

To enhance user convenience, the app uses TokenAuthentication and social-oauth2, allowing users to register and log in seamlessly with their Google or Apple ID accounts.

 ## Tools used in project:

<p align=center>
<a href="https://www.python.org"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="60" height="60"/></a> 
<a href="https://www.djangoproject.com/"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="60" height="60"/> </a>
<a href="https://git-scm.com/"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" alt="git" width="60" height="60"/> </a> 
<a href="https://www.postgresql.org.pl/"> <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/postgresql/postgresql-original-wordmark.svg" alt="psql" width="60" height="60"/> </a>
<a href="https://www.docker.com/"> <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/docker/docker-original-wordmark.svg" alt="docker" width="60" height="60"/> </a>
<a href="https://redis.io/"> <img src="https://github.com/devicons/devicon/blob/master/icons/redis/redis-original-wordmark.svg" alt="redis" width="60" height="60"/> </a>

</p>
<p align=center>
<a href="https://python-poetry.org/"> <img src="https://github.com/python-poetry/website/blob/main/static/images/logo-origami.svg" alt="redis" width="60" height="60"/> </a>
<a href="https://swagger.io/"> <img src="https://github.com/devicons/devicon/blob/master/icons/swagger/swagger-original.svg" alt="swagger" width="60" height="60"/> </a>
<a href="https://nginx.org/en/"> <img src="https://github.com/devicons/devicon/blob/master/icons/nginx/nginx-original.svg" alt="nginx" width="60" height="60"/> </a>
<a href="#"> <img src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original.svg" alt="html" width="60" height="60"/> </a>
<a href="#"> <img src="https://github.com/devicons/devicon/blob/master/icons/css3/css3-original.svg" alt="css" width="60" height="60"/> </a>
<a href="https://www.cloudflare.com/"> <img src="https://github.com/devicons/devicon/blob/master/icons/cloudflare/cloudflare-original-wordmark.svg" alt="cloudflare" width="60" height="60"/> </a>
</p>
<br>  

## Features
- [x] [user management](#user-management)
- [x] [trip management](#trip-management)
- [x] [toggle trip view](#toggle-trip-view)
- [x] [expense management](#expense-management)
- [x] [set base currency](#set-base-currency)
- [x] [purchase a premium version](#purchase-a-premium-version) 


## User management
- Traditional Registration:
Users can sign up by providing their email and password. After registration, they will receive an activation link via email. Clicking this link activates their account and grants access to the platform.
<p align="center"><img src="" width="253" height="549"/></p>

- Simplified Registration:
For a faster and more convenient experience, users can register and log in using Google Sign-In or Apple Sign-In, skipping the need for manual account activation.
<p align="center"><img src="" width="253" height="549"/></p>

- Password Recovery:
If users forget their password, they can easily recover it by requesting a 5-digit token, which will be sent to their registered email address. This token can be used to securely reset their password.
<p align="center"><img src="" width="253" height="549"/></p>

- Password Management:
Users who registered traditionally can change their password at any time through the application settings.
<p align="center"><img src="" width="253" height="549"/></p>

[Go to top](#top) 

## Trip management
Adding/Editing/Deleting a Trip:
Users can create a new trip by providing a name, selecting one of the available default images, and adding the countries they plan to visit. Users can then edit a trip by clicking the edit icon in the top-right corner of the trip view. There are also two ways to delete a specific trip: either during the editing process or by simply swiping left on the trip in the main screen for quick deletion.
<p align="center">
  <img src="" width="253" height="549"/>
  <img src="" width="253" height="549"/>
  <img src="" width="253" height="549"/>
</p>

[Go to top](#top) 

## Toggle trip view
Users can use a switch on the main screen of the application to toggle between two trip views: normal view with all information and detailed view without images, providing a more streamlined and detailed list.
<p align="center">
  <img src="" width="253" height="549"/>
  <img src="" width="253" height="549"/>
</p>

[Go to top](#top) 

## Expense management
Adding/Editing/Deleting an Expense:
Users can add an expense to a trip by providing details such as the name, amount, currency, and category. Every expense can be edited by tapping on it in the expense list. Users can delete an expense in two ways: either during the editing process or by swiping left on the expense in the list for quick deletion.

Note: The value of each expense is displayed in the currency it was originally added in. However, for the total trip expenses, each expense is automatically converted to the base currency, which can be configured by the user in the application settings.
<p align="center">
  <img src="" width="253" height="549"/>
  <img src="" width="253" height="549"/>
  <img src="" width="253" height="549"/>
</p>

[Go to top](#top) 

## Set base currency
In the main settings of the application, users can set their **base currency**. All expenses will be automatically converted to this base currency. This allows users to see the total cost of each trip on the main screen in their chosen base currency, providing a more convenient and consistent view for better user experience. User can change the **base currency** at any time.
<p align="center">
  <img src="" width="253" height="549"/>
  <img src="" width="253" height="549"/>
</p>

[Go to top](#top) 

## Purchase a premium version
In the main settings, users can also purchase a lifetime premium version of the app. With the premium version, users will enjoy an ad-free experience and have access to unlimited features, without any restrictions.
<p align="center">
  <img src="" width="253" height="549"/>
  <img src="" width="253" height="549"/>
</p>

[Go to top](#top) 
