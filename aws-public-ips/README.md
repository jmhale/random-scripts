#AWS Public IP Lookup

###Description
Performs a look up of all Elastic Network Interfaces in a AWS account/region and outputs them along with either their instance ID or description, depending on the resource that it's attached to.


###Usage
```
pip install -r requirements.txt
python aws_public_ips.py [-s]
```


###Shodan
Will optionally perform a Shodan Host Search on all IPs it finds, if the `-s` or `--shodan` flag is provided. You'll need to have a Shodan API key and export it to the `SHODAN_API_KEY` environment variable for this feature to work.

Be mindful of your scan credits in Shodan if you have a lot of public facing IPs!