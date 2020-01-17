# Ze Emailer
A complete email tool that helps generate emails from people's name and surname for growth hacking.

# Configuration

The main configuration parameters for the application can be found in the `ze_mailer.app.core.settings` module. It returns an Ordered Dictionnary of values.

They are wrapped within he `Configuration` class and then initialized or instanciated in the `configuration` parameter.

For instance, if you want to add or change a parameter you would do the following:

```
configuration[my_configuration] = my_value
```

You can also retrieve values just like as you would with a dictionnary by doing this:

```
item = configuration[key]
```

## Calling the instance

As seen above, you can change items by passing a key and a value. However, you can also call the instance and pass JSON file path containing variables:

```
new_settings = configuration(file_path=path_to_file)
```

This returns an updated version of the settings.

# Sending emails
## Servers

The application comes with custom email server that you can use to send emails using Gmail or Outlook. They derive from the `BaseServer` class which you can subclass to create a custom server of your own.

You can initialize a server using two methods: __configuration__ or __class parameters__.

```
from ze_mailer.app.core.settings import configuration
from ze_mailer.app.core.servers import Gmail

configuration['user'] = 'email@gmail.com'
configuration['password'] = 'gmail'

server = Gmail()
```

```
from ze_mailer.app.core.servers import Gmail

server = Gmail(user=email@gmail.com, password=gmail)
```

__NOTE:__ Servers aren't to be used directly though you can if you want to. They are to be subclassed by a class that will serve as the main entrypoint for sending emails.

# Senders

These classes are responsible for sending emails using Gmail, Outlook or your custom server to the users.

You can send and email with or without an attachment using one of the following classes.

## Setting the credentials

Before sending your emails, you need to set the credentials. You can do so in three ways:

```
from ze_mailer.app.core.settings import configuration
from ze_mailer.app.core.senders import SendEmail

configuration['user'] = 'email@gmail.com'
configuration['password'] = 'gmail'

sender = SendEmail('from_email@gmail.com', 'to_email@gmail.com', 'Welcome to Mars')
```

As you can see, the first method uses the configuration dictionnary to set the user and the password.

With the second method, you can also pass the user and password in the keyword arguments of the email sender:

```
from ze_mailer.app.core.settings import configuration
from ze_mailer.app.core.senders import SendEmail

sender = SendEmail('from_email@gmail.com', 'to_email@gmail.com', 'Welcome to Mars', user='user', password='password')
```

Finally, with the last method, you can set environment variables using `ZEMAILER_USER` and `ZEMAILER_PASSWORD` to the values that you want.

The important thing to understand is the server will search for the credentials in these three places before calling the `CredentialsError` if user and password are not set.

The search order is the following: user provided > configuration > environment.

## Sending the email

Once you've called the __SendEmail__ or __SendEmailWithAttachment__ class, the email is then automatically sent using the \_\_init\_\_. 

# Generating emails

Suppose you have a list of names and you want to generate emails from that list in order to send. Here's how you can proceed.

The main class for generating emails can be found in __ze_emailer.app.patterns__. It is composed of three main modules but the one that will interest us is the __base module__.

There are two ways to generate emails:

    - NamePatterns
    - SimpleNamesAlgorithm

## Subclassing NamesPatterns

This class was created with the specific objective of being able to create custom email generation classes.

For instance, let's say we wanted to create a custom class for _myenterprise.fr_:

```
class MyEnterprise(NamesPatterns):
    pattern = name.surname
    domain = myenterprise.fr
    particle = None

MyEnterprise(file_path=/path/to/file)
```

It's that easy! By executing the class, we can get emails from names such as `name.surname@myenterprise.fr`

## Using SimpleNamesAlgorithm

There might be cases where you do not want to create a custom class but just want to generate emails inline. In which case, the simple names algorithm does exactly that.

```
from ze_emailer.app.patterns.algorithms import SimpleNamesAlgorithm

SimpleNamesAlgorithm(path/to/file, separators=[., -, _], domains=[gmail, outlook])
```
The result is then exactly the same as using the NamesPatterns as a super class.