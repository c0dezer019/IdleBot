# EnforcerBot

Most Discord bots that I've seen do not provide actual user activity levels. I wanted to build a bot that monitors user idle times as well as
automatically boot the user if idle for x amount of time. The bot is written in Python and will use threading to ensure that it performs reasonably. It will feature rich settings that server admin can set to ensure the bot only performs in a controlled, expected way desired by server admin.

## Features

- Long-term data persistence with PostgreSQL.
- Logs user activity timestamps in the channels that it can see.
- Calculates user idle times based off timestamp of last activity.
- Flags a user as active or inactive based on a set idle time.
- Sets an inactive role on inactive users.
- Rich setting options settable by server admin.

## **Usage Guide**

Upon invitation to the server, the bot will catalogue every user on the server, storing their user 18-digit id and name w/ discriminator in order to tell one user from another. The bot uses the id to ensure quality of activity tracking. A Nitro user changing their discriminator could cause potential conflicts.

The bot only stores the type, location, and timestamp of last activity and nothing else beyond a user's Discord identity.

### **Commands**

By default, commands are prefixed with a ? like many options, this can be changed if it ends up conflicting with the prefix of another bot with a similar command.

#### **?setup**

This command is only performable by server admin or users with the proper role. It is preferred that only admin use this command. Use case of this command will be rare. In the event the bot fails to perform it's on_guild_join() script correctly, this should be reported to the bot owner. Upon fix of said error, perform this command to initiate it manually without having to kick and re-invite the bot.

*This is only a temporary command until I can think of a better use of the API to do this automatically.*

#### **?set <setting> <\*args>**

This command will set the desired settings with the specified values separated by spaces.

#### **?check <channel/user>**

Checks the idle time from last activity for the specified entity.

#### **?warn <user> <msg>**

If for some reason you want to warn a user on activity levels before the bot does, this is how you do it. The msg is temporary, the bot will have its own default warning message.
