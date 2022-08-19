### Example Server to Server App

This app is intended as a demonstration of how to use the [29 Next App Framework](https://developers.29next.com/apps/) in a "server to server" context.

#### Features

* [Oauth Setup Flow](https://developers.29next.com/apps/oauth/)
* [Session Token Login](https://developers.29next.com/apps/oauth/session-auth/)
* [Admin API access and scopes](https://developers.29next.com/api/admin/)
* [Webhooks](https://developers.29next.com/webhooks/) setup, data validation, and `app.uinstalled` event handling.


### How to Setup

This app uses [Django](https://docs.djangoproject.com/en/4.1/intro/install/), you can follow Django install guides to insure you have Python in your local environment.

#### Create App In Partner Account
The first step is to create an App in your 29 Next Partner Account. You'll need your app Client ID and Client Secret later on in the setup process.

#### Install Dependencies
```
pip install -r requirements.txt
```
#### Setup Public Tunnel

To access your localhost for app development, you can use [Ngrok](https://ngrok.com/) or [LocalTunnel](https://localtunnel.github.io/www/) to create and open a public tunnel to your local machine.

#### Environment Variables

| Variable | Description|
|--- | --- |
|APP_DOMAIN| Your domain when running the app (ie your public tunnel url).|
|CLIENT_ID| Your App Client ID found in your partner account. |
|CLIENT_SECRET| Your App Client Secret found in your partner account. |

To run this Django project, you'll need to set environment variables with your local app domain, app client id and client secret (from your 29 Next app).

```
export <VARIABLE>=<VALUE>
```

#### Run Django App

To run the Django app on your local, use the following command.

*Django port needs to match the public tunnel port.*

```
python manage.py runserver 0.0.0.0:<PORT>
```

#### Push Your App

You can now use [App Kit](https://developers.29next.com/apps/app-kit/) to create your [App Manifest](https://developers.29next.com/apps/manifest/) to your partner account and link your development store to your app.

##### App Manifest.json
*Replace the domain with your local domain path.*
```
{
  "oauth": {
    "app_url": "{YOUR APP DOMAIN }/stores/auth/login/",
    "redirect_urls": [
      "{YOUR APP DOMAIN }/stores/auth/setup/"
    ]
  }
}

```

With your configured manifest.json, you can now build and push your app to your account.
```
nak build && nak push
```

#### Install on Development Store
You can now connect your app to your development store which will initiate the Oauth setup flow configure Admin API access.
