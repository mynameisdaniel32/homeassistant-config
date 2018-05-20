Check forecast for today and tomorrow

Check rain for today

if not enough rainfall

Turn on sprinklers for kX duration

Where X is a standard constant for each zone to get 20mm of water per week of normal temp

And K scales based on the following factors:
 - temperature
 - cloud coverage
 - existing soil moisture (based on sensor or last sprinkler output
 
 
Info required:
 - temp today
 - rainfall today
 - predicted rainfall tomorrow
 - probability of rainfall tomorrow
 - temp tomorrow
 - time since last run
 - current soil moisture
 
 - switch.sprinkler_zone_1-8
 - trigger time
 - max duration (limit)
 - min duration (limit)

#K_T scale factor for duration:
	kT = 
		if (PWS(today temp) <= 25)
			= 1
		if (PWS(today temp) > 25)
			= 0.05 * PWS(today temp) - 0.2
 
#Reducing factor based on rainfall today
	kR = PWS(rainfall today)

#Reducing factor based on predicted rainfall
	kP = PWS(tomorrow predicted rainfall) * PWS(tomorrow rainfall probability)

#Combined K factors
	Required water = (1/7) * kT * X - kR - 0.8 * kP