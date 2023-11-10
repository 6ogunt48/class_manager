 class manager app
 a student-teacher portal API that allows teachers and students to sign up and interact within their respective classes

To Test out API in local development mode - You need ckone the repository locally and  to have docker installed 

At the root of the project where the docker-compose file is located .Kindly run 

``` docker-compose build ```

once this is running this will build up the cntainers of both the application and database. once done, we can now start our service by using

``` docker-compose up ```

once our containers are running please run this code in your browser to see api docs and test endpoints 

```http://localhost:8004/docs ```



![Continuous Integration and Delivery](https://github.com/6ogunt48/class_manager/actions/workflows/main.yml/badge.svg?branch=main)
