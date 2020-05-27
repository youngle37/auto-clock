# Auto clock in/out on NCU HumanSys

## Dependency
 - Python3
 - requests
 - lxml

## Usage

```
usage: python3 clock.py [-h] [--config CONFIG] [-j JOBNAME] {signin,signout}

positional arguments:
  {signin,signout}

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       default: config.json
  -j JOBNAME, --jobname JOBNAME
                        欲打卡工作名稱，定義在 config.json (default: default_job)
```

## How to Use
 1. 
    Make sure you have installed the dependencies.
    ```
      $ pip3 install requests lxml
    ```

 2.
    Create config.json
    ```
      $ cp config.json.example config.json
    ``` 

 3. Config.json format example
   ```json
{
    "account": "",
    "password": "",
    "jobs":
    {
       "default_job":
        {
            "partTimeId": "Get from the url of the page you clock in/out",
            "attendWork": "值班"
        },
        "example_job1":
        {
            "partTimeId": "111999",
            "attendWork": "值班 & 開發"
        },
        "example_job2":
        {
            "partTimeId": "119999",
            "attendWork": "玩"
        }
    }
}
   ```

 3. 
    Set these parameters in config.json

    | Parameters             | description                                                   |
    |------------------------|---------------------------------------------------------------|
    | account                | Account on Portal                                             |
    | password               | Password on Portal                                            |
    | jobs                   | Jobs list, jobName => partTimeId and attendWork               | 
    | partTimeId             | Get from the url of the page you clock in/out                 |
    | attendWork             | Job content                                                   |

 4.
    Set the script executable.
    ```
        $ sudo chmod 777 Auto_clock/clock.py
    ```

 5.
    Time calibration.

 6.
    Config the crontab.
    ```
      $ crontab -e

      #   minute   hour  day   month dayofweek  COMMAND
         0        8     1-7   *     *           python3 /PATH/TO/Auto_clock/clock.py signin 
         2        18    1-7   *     *           python3 /PATH/TO/Auto_clock/clock.py signout

         0        8     1-7   *     *           python3 /PATH/TO/Auto_clock/clock.py -j example_job1 signin 
         2        18    1-7   *     *           python3 /PATH/TO/Auto_clock/clock.py -j example_job1 signout

         0        8     1-7   *     *           python3 /PATH/TO/Auto_clock/clock.py -j example_job2 signin 
         2        18    1-7   *     *           python3 /PATH/TO/Auto_clock/clock.py -j example_job2 signout        
      # For example, 50 hours per month per jobs.    
    ```

