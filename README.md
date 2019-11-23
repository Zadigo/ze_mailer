# ze_mailer
A complete email tool for growth hacking


# Emails
## Servers

The application comes with custom emeail servers that you can use to send emails using Gmail or Outlook. They derive from the `BaseServer` class which you can subclass to create a custom server of your own.

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

server = Gmail(user='email@gmail.com', password='gmail')
```

__NOTE:__ Servers aren't to be used directly though you can if you want to. They are to be subclassed by a class that will server as the main entrypoint for sending emails.

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

Use the method that suits you best.

## Sending the email

Once you've called the __SendEmail__ or __SendEmailWithAttachment__ class, the email is then automatically sent using the \_\_init\_\_. 