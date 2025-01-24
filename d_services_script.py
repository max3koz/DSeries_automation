import argparse
import datetime
import json
import math
import os
import re
import requests
import sys
import time
import urllib

debug = True

outputPath = __file__.replace(os.path.basename(__file__), "")
logFileName = "d-services_testing_" + datetime.datetime.today().strftime("%Y-%m-%d_%H-%M")[:10] + ".log"
#logPath = "C:\\Imagine\\1 - Software\\Windows\\NPCM-Tools\\d-services\\Log\\" + logFileName
logPath = "E:\\d-services\\Log\\" + logFileName

logFile = open(logPath, "a")
logFile.write("\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ")
logFile.close()

# Sydney summer time
#tzOffset = 90000 * 11
# Sydnet winter time
tzOffset = 90000 * 10

########################################################################################################################################################################################################
# header end
########################################################################################################################################################################################################

########################################################################################################################################################################################################
# functions start
########################################################################################################################################################################################################
# write log message to the log file
def logWriter(message, printed):
    if printed == True:
        print("    " + message)
    logFileName = "d-services_testing_" + datetime.datetime.today().strftime("%Y-%m-%d_%H-%M")[:10] + ".log"
    # logPath = "C:\\Imagine\\1 - Software\\Windows\\NPCM-Tools\\d-services\\Log\\" + logFileName
    logPath = "E:\\d-services\\Log\\" + logFileName
    logFile = open(logPath, "a")

    logFile.write("\n" + datetime.datetime.today().strftime("%Y-%m-%d : %H:%M:%S.%f")[:24] + " : " + message)

    logFile.close()


def busName2Number(dServicesEndointName, busName):

    logWriter("System name = [%s], Bus Name = [%s]" % (dServicesEndointName, busName), False)

    systemABuses = {"77SYD" : "1", "77MEL" : "2", "77BRI" : "3", "77ADE" : "4", "77PER" : "5", "77GLD" : "6", "77QCNS" : "7", "77QTSV" : "8", "77QMKY" : "9", "77QRKY" : "10", "77QWBY" : "11", "77QSSC" : "12", "77QTWB" : "13", "72SYD" : "25", "72MEL" : "26", "72BRI" : "27", "72ADE" : "28", "72PER" : "29", "72QLD" : "30", "72QTSV" : "31", "72QMKY" : "32", "72QRKY" : "33", "72QWBY" : "34", "72QSSC" : "35", "72QTWB" : "36", "7MSYD" : "49", "7MMEL" : "50", "7MBRI" : "51", "7MADE" : "52", "7MPER" : "53", "7MQCNS" : "54", "7MQTSV" : "55", "7MQMKY" : "56", "7MQRKY" : "57", "7MQWBY" : "58", "7MQSSC" : "59", "7MQTWB" : "60", "7XSYD" : "73", "7XMEL" : "74", "7XBRI" : "75", "7XADE" : "76", "7XPER" : "77", "7XQLD" : "78", "7FSYD" : "79", "7FMEL" : "80", "7FBRI" : "81", "7FADE" : "82", "7FPER" : "83", "7FQLD" : "84", "7AUX1" : "97", "7AUX2" : "98", "7AUX3" : "99", "7AUX4" : "100", "7AUX5" : "101", "7AUX6" : "102", "7NET1" : "103", "7NET2" : "104", "7NET3" : "105", "7NET4" : "106", "7AUX7" : "107", "7AUX8" : "108", "S7DAR" : "121", "S7LAU" : "122", "S7HOB" : "123", "S7PTP" : "124", "S7PLB" : "125", "S7VAN" : "126", "S7VAS" : "127", "S2DAR" : "128", "S2TAS" : "129", "S2SPG" : "130", "S2VAN" : "131", "S2VAS" : "132", "SMDAR" : "133", "SMVST" : "134", "SMTAS" : "135", "SMSPG" : "136", "KEEP-LF" : "118", "KEEP-SF" : "119"}
    systemBBuses = {"SYD-GEM" : "1", "MEL-GEM" : "2", "BRI-GEM" : "3", "DAR-GEM" : "4", "ADE-GEM" : "5", "PER-GEM" : "6", "NEW-GEM" : "7", "TAM-GEM" : "8", "COF-GEM" : "9", "LIS-GEM" : "10", "CEN-GEM" : "11", "TPM-GEM" : "12", "GLD-GEM" : "13", "SGSPG" : "14", "9AUX01" : "22", "9AUX02" : "23", "9AUX03" : "24", "9KEEP1" : "32", "SYD-NINE" : "33", "MEL-NINE" : "34", "BRI-NINE" : "35", "GCO-NINE" : "36", "DAR-NINE" : "37", "ADE-NINE" : "38", "PER-NINE" : "39", "NEW-NINE" : "40", "TAM-NINE" : "41", "COF-NINE" : "42", "LIS-NINE" : "43", "CEN-NINE" : "44", "TPM-NINE" : "45", "GLD-NINE" : "46", "S9PTP" : "47", "S9PLB" : "48", "9AUX04" : "54", "9AUX05" : "55", "9AUX06" : "56", "9KEEP2" : "63", "SYD-GO" : "65", "MEL-GO" : "66", "BRI-GO" : "67", "DAR-GO" : "68", "ADE-GO" : "69", "PER-GO" : "70", "NEW-GO" : "71", "TAM-GO" : "72", "COF-GO" : "73", "LIS-GO" : "74", "CEN-GO" : "75", "TPM-GO" : "76", "GLD-GO" : "77", "SOSPG" : "78", "9AUX07" : "85", "9AUX08" : "86", "9AUX09" : "87", "9AUX10" : "88", "9KEEP3" : "95", "SYD-LIFE" : "97", "MEL-LIFE" : "98", "BRI-LIFE" : "99", "DAR-LIFE" : "100", "ADE-LIFE" : "101", "PER-LIFE" : "102", "NEW-LIFE" : "103", "TAM-LIFE" : "104", "COF-LIFE" : "105", "LIS-LIFE" : "106", "CEN-LIFE" : "107", "TPM-LIFE" : "108", "GLD-LIFE" : "109", "SLSPG" : "110", "SYD-RUSH" : "111", "MEL-RUSH" : "112", "BRI-RUSH" : "113", "ADE-RUSH" : "114", "PER-RUSH" : "115", "NSW-RUSH" : "116", "ASPIRE" : "117", "9KEEP4" : "127"}
    systemCBuses = {"STCNS" : "33", "STTSV" : "34", "STMKY" : "35", "STRKY" : "36", "STWBY" : "37", "STSSC" : "38", "STTWB" : "39", "STORG" : "40", "STWAG" : "41", "STWOL" : "42", "STCAN" : "43", "STSTH" : "44", "STALB" : "45", "STSHP" : "46", "STBEN" : "47", "STBAL" : "48", "STGIP" : "49", "STTAS" : "50", "STPTP" : "51", "STPLB" : "52", "STDAR" : "53", "STVAN" : "54", "STVAS" : "55", "SPCNS" : "97", "SPTSV" : "98", "SPMKY" : "99", "SPRKY" : "100", "SPWBY" : "101", "SPSSC" : "102", "SPTWB" : "103", "SPORG" : "104", "SPWAG" : "105", "SPWOL" : "106", "SPCAN" : "107", "SPSTH" : "108", "SPALB" : "109", "SPSHP" : "110", "SPBEN" : "111", "SPBAL" : "112", "SPGIP" : "113", "SPTAS" : "114", "SPSPG" : "115", "SPDAR" : "116", "SPVAN" : "117", "SPVAS" : "118", "SBCNS" : "161", "SBTSV" : "162", "SBMKY" : "163", "SBRKY" : "164", "SBWBY" : "165", "SBSSC" : "166", "SBTWB" : "167", "SBORG" : "168", "SBWAG" : "169", "SBWOL" : "170", "SBCAN" : "171", "SBSTH" : "172", "SBALB" : "173", "SBSHP" : "174", "SBBEN" : "175", "SBBAL" : "176", "SBGIP" : "177", "SBTAS" : "178", "SBSPG" : "179", "SBDAR" : "180", "SBVST" : "181", "SSCNS" : "225", "SSTSV" : "226", "SSMKY" : "227", "SSRKY" : "228", "SSWBY" : "229", "SSSSC" : "230", "SSTWB" : "231", "SSORG" : "232", "SSWAG" : "233", "SSWOL" : "234", "SSCAN" : "235", "SSSTH" : "236", "SSALB" : "237", "SSSHP" : "238", "SSBEN" : "239", "SSBAL" : "240", "SSGIP" : "241", "SSTAS" : "242", "TAUX11" : "272", "TAUX12" : "273", "TAUX13" : "274", "TAUX14" : "275"}
    systemTBuses = {"AUX1" : "97", "AUX2" : "98", "AUX3" : "99", "AUX4" : "100"}

    try:
        if   dServicesEndointName == "NPCA1" or dServicesEndointName == "NPCA2" or dServicesEndointName == "TBSA1" or dServicesEndointName == "TBSA2":
            busId = systemABuses[busName]
        elif dServicesEndointName == "NPCB1" or dServicesEndointName == "NPCB2" or dServicesEndointName == "TBSB1" or dServicesEndointName == "TBSB2":
            busId = systemBBuses[busName]
        elif dServicesEndointName == "NPCC1" or dServicesEndointName == "NPCC2" or dServicesEndointName == "TBSC1" or dServicesEndointName == "TBSC2":
            busId = systemCBuses[busName]
        elif dServicesEndointName == "TEST":
            busId = systemTBuses[busName]
        else:
            busId = "None"

    except KeyError:
        busId = "None"
        logWriter("Bus [%s] not found on System [%s]" % (busName, dServicesEndointName), True)
        exit()

    logWriter("System name = [%s], Bus Name = [%s], Bus ID = [%s]" % (dServicesEndointName, busName, busId), False)

    return busId


def timeToFrames(time):

    hoursAsFrame   = int(time[0:2]) * 90000
    minutesAsFrame = int(time[3:5]) * 1500
    secondsAsFrame = int(time[6:8]) * 25

    try:
        framesAsFrame = int(time[9:11])
    except:
        framesAsFrame = 0

    frameCount   = hoursAsFrame + minutesAsFrame + secondsAsFrame + framesAsFrame
    frameCountTz = hoursAsFrame + minutesAsFrame + secondsAsFrame + framesAsFrame + tzOffset

    return frameCount, frameCountTz


def framesToTime(frameCount):

    hoursAsText = math.floor(frameCount / 90000)
    if hoursAsText > 23:
        hoursAsText -= 24
    hoursAsText = ("0" + str(hoursAsText))[-2:]

    return hoursAsText + ":" + ("0" + str(math.floor((frameCount % 90000) / 1500)))[-2:] + ":" + ("0" + str(math.floor((frameCount % 1500) / 25)))[-2:]


def initSession():
    logWriter("Initialising D-Service session", False)
    url = dServicesEndoint + "sessions"
    logWriter("D-Services URL = [%s]" % url, False)

    headers = {'Content-Type': 'application/json'}

    params = {
        'user name': '',
        'password': ''
    }

    logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    body = '{"properties": {"schedule window": 16, "as-run log window": 16} }'
    logWriter("Session configuration = [%s]" % body, False)

    try:
        sessionResponse = requests.post(url, params=params, headers=headers, data=body)

    except ConnectionRefusedError:
        logWriter("Connection refused [%s]" % (url), True)
        exit()

    logWriter("Session Response Status Code = [%s]" % str(sessionResponse.status_code), False)
    #print("    Session Response Content = [%s]" % sessionResponse.content)
    sessionResponseBody = sessionResponse.text
    logWriter("session Response Body = [%s]" % sessionResponseBody, False)
    sessionResponseParsed = json.loads(sessionResponseBody)

    sessionId = sessionResponseParsed['session']

    return sessionId


def pingSession(sessionId):
    logWriter("Pinging a D-Service session", False)
    url = dServicesEndoint + "sessions/session"
    logWriter("D-Services URL = [%s]" % url, False)

    headers = {'Content-Type': 'application/json'}

    params = {
        'session': sessionId
    }

    logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    sessionResponse = requests.get(url, params=params, headers=headers)
    logWriter("Session Response Status Code = [%s]" % str(sessionResponse.status_code), True)
    #print("    Session Response Content = [%s]" % sessionResponse.content)
    sessionResponseBody = sessionResponse.text
    logWriter("session Response Body = [%s]" % sessionResponseBody, True)


def deleteSession(sessionId):
    logWriter("Deleting the D-Services session", False)
    url = dServicesEndoint + "sessions/" + sessionId
    logWriter("D-Services URL = [%s]" % url, False)

    headers = {'Content-Type': 'application/json'}

    #params = {
    #    'session': sessionId
    #}
    #logWriter("Params = [%s]" % str(params), False)
    #params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    #sessionResponse = requests.delete(url, params=params, headers=headers)
    sessionResponse = requests.delete(url, headers=headers)
    logWriter("Session Response Status Code = [%s]" % str(sessionResponse.status_code), False)
    if str(sessionResponse.status_code) == "200":
        logWriter("Session [%s] deleted successfully" % sessionId, True)
    else:
        print("    Session Response Content = [%s]" % sessionResponse.content)
        sessionResponseBody = sessionResponse.text
        logWriter("Session Response Body = [%s]" % sessionResponseBody, True)


def getBuses(sessionId):
    logWriter("Getting a list of all system buses", False)
    url = dServicesEndoint + "buses"
    logWriter("D-Services URL = [%s]" % url, False)

    params = {
        'session': sessionId
    }

    logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    busesResponse = requests.get(url, params=params)
    logWriter("Bus List Response Status Code = [%s]" % str(busesResponse.status_code), False)
    #print("    Bus List Response Content = [%s]" % busesResponse.content)
    busesResponseBody = busesResponse.text
    logWriter("Bus List Response Body = [%s]" % busesResponseBody, False)
    busesResponseParsed = json.loads(busesResponseBody)

    return busesResponseParsed


def getBusConfig(sessionId, busId):
    logWriter("Getting the configuration of a bus", False)
    url = dServicesEndoint + "buses/" + busId + "/configuration"
    logWriter("D-Services URL = [%s]" % url, False)

    params = {
        'session': sessionId
    }

    logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    busConfigResponse = requests.get(url, params=params)
    logWriter("Bus Config Response Status Code = [%s]" % str(busConfigResponse.status_code), False)
    #print("    Bus Config Response Content = [%s]" % busConfigResponse.content)
    busConfigResponseBody = busConfigResponse.text
    logWriter("Bus Config Response Body = [%s]" % busConfigResponseBody, False)
    busConfigResponseParsed = json.loads(busConfigResponseBody)

    return busConfigResponseParsed


def getEvents(sessionId, busId, isAsRun):
    if isAsRun == True:
        isAsRunText = "as-run-log"
    else:
        isAsRunText = "schedule"
    logWriter("Getting a list of [" + isAsRunText + "] events currently on the bus", False)
    url = dServicesEndoint + "buses/" + busId + "/" + isAsRunText
    if debug:
        logWriter("D-Services URL = [%s]" % url, False)

    params = {
        'session': sessionId,
        'subscribe': 'false'
    }

    if debug:
        logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    eventsResponse = requests.get(url, params=params)
    logWriter("Events Response Status Code = [%s]" % str(eventsResponse.status_code), False)
    #print("    Events Response Content = [%s]" % eventsResponse.content)
    eventsResponseBody = eventsResponse.text
    if debug:
        logWriter("Events Response Body = [%s]" % eventsResponseBody, False)
    eventsResponseParsed = json.loads(eventsResponseBody)

    return eventsResponseParsed


def getAnEvent(sessionId, busId, eventId):
    if debug:
        logWriter("Getting the details of event [" + eventId + "]", False)
    url = dServicesEndoint + "buses/" + busId + "/events/" + eventId
    if debug:
        logWriter("D-Services URL = [%s]" % url, False)

    params = {
        'session': sessionId,
        'subscribe': 'false'
    }

    if debug:
        logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    eventResponse = requests.get(url, params=params)
    if str(eventResponse.status_code) == "200":
        pass
    else:
        logWriter("Event Response Status Code = [%s]" % str(eventResponse.status_code), False)
    #print("    Event Response Content = [%s]" % eventResponse.content)
    eventResponseBody = eventResponse.text
    if debug:
        logWriter("Event Response Body = [%s]" % eventResponseBody, False)
    eventResponseParsed = json.loads(eventResponseBody)

    if eventResponse.status_code == 200:

        try:
            eventUTC_DATE = eventResponseParsed['data']['primary']['UTC_DATE']
        except:
            logWriter("Event Response Content = [%s]" % eventResponse.content, True)
            eventResponseParsed['data']['primary']['UTC_DATE'] = ""

        try:
            eventUTC_TIME = eventResponseParsed['data']['primary']['UTC_TIME']
        except:
            eventResponseParsed['data']['primary']['UTC_TIME'] = ""

        try:
            eventTYPE_MATERIAL = eventResponseParsed['data']['primary']['TYPE_MATERIAL']
        except:
            eventResponseParsed['data']['primary']['TYPE_MATERIAL'] = ""

        try:
            eventSEGMENT = eventResponseParsed['data']['primary']['SEGMENT']
        except:
            eventResponseParsed['data']['primary']['SEGMENT'] = ""

        try:
            eventSOURCE = eventResponseParsed['data']['primary']['SOURCE']
        except:
            eventResponseParsed['data']['primary']['SOURCE'] = ""

        try:
            eventITEM = eventResponseParsed['data']['primary']['ITEM']
        except:
            eventResponseParsed['data']['primary']['ITEM'] = ""

        try:
            eventDURATION = eventResponseParsed['data']['primary']['DURATION']
        except:
            eventResponseParsed['data']['primary']['DURATION'] = ":  :  :"

        try:
            eventTITLE = eventResponseParsed['data']['primary']['TITLE']
        except:
            eventResponseParsed['data']['primary']['TITLE'] = ""

        try:
            eventCOMMENTS = eventResponseParsed['data']['primary']['COMMENTS']
        except:
            eventResponseParsed['data']['primary']['COMMENTS'] = ""

        try:
            eventTONE_PROG_ID = eventResponseParsed['data']['primary']['TONE_PROG_ID']
        except:
            eventResponseParsed['data']['primary']['TONE_PROG_ID'] = ""

        try:
            eventTONE_SPLICE_ID = eventResponseParsed['data']['primary']['TONE_SPLICE_ID']
        except:
            eventResponseParsed['data']['primary']['TONE_SPLICE_ID'] = ""

        try:
            eventBREAK_RLYS = eventResponseParsed['data']['primary']['BREAK_RLYS']
        except:
            eventResponseParsed['data']['primary']['BREAK_RLYS'] = ""

        try:
            eventAFFILIATE_BREAK_RLYS = eventResponseParsed['data']['primary']['AFFILIATE_BREAK_RLYS']
        except:
            eventResponseParsed['data']['primary']['AFFILIATE_BREAK_RLYS'] = ""

        try:
            eventBREAK_RLYS_3 = eventResponseParsed['data']['primary']['BREAK_RLYS_3']
        except:
            eventResponseParsed['data']['primary']['BREAK_RLYS_3'] = ""

        try:
            eventEVENT_TYPE = eventResponseParsed['data']['primary']['EVENT_TYPE']
        except:
            eventResponseParsed['data']['primary']['EVENT_TYPE'] = ""


        return eventResponseParsed

    else:

        return eventResponse.status_code


def getOnAirEvent(sessionId, busId):
    logWriter("Getting the On-Air event", False)
    url = dServicesEndoint + "buses/" + busId + "/on-air-event"
    logWriter("D-Services URL = [%s]" % url, False)

    params = {
        'session': sessionId,
        'subscribe': 'false'
    }

    logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    onAirEventResponse = requests.get(url, params=params)
    logWriter("Event Response Status Code = [%s]" % str(onAirEventResponse.status_code), False)
    #print("    Event Response Content = [%s]" % onAirEventResponse.content)
    onAirEventResponseBody = onAirEventResponse.text
    logWriter("Event Response Body = [%s]" % onAirEventResponseBody, False)
    onAirEventResponseParsed = json.loads(onAirEventResponseBody)

    return onAirEventResponseParsed


def selectEventFields(sessionId):
    logWriter("Setting the desired fields to be returned in the event query", False)
    url = dServicesEndoint + "fields"
    logWriter("D-Services URL = [%s]" % url, False)

    headers = {'Content-Type': 'application/json'}

    params = {
        'session': sessionId,
        'subscribe': 'false'
    }

    # System C doesn't have break_rlys_3 so use old field layout request
    if fieldList == "OLD":
        body = '{"fields": {"primary": ["UTC_DATE", "UTC_TIME", "SOURCE", "START_TYPE", "END_TYPE", "ITEM", "TITLE", "TYPE_MATERIAL", "COMMENTS", "BREAK_RLYS", "SEGMENT", "DURATION", "TEXTOUT1", "PROGRAM_CLASS", "AUDIO_MODE_1", "EVENT_TYPE", "EVENT_NUM", "CUE_COUNTDOWN", "RELEASED", "SOURCE", "UNIQUE_EVENT_ID", "TONE_PROG_ID", "AFFILIATE_BREAK_RLYS", "TONE_SPLICE_ID"], "subsidiary": [{"key": {"type": "Protection"}, "value":["SRC"]}]}}'
    else:
        body = '{"fields": {"primary": ["UTC_DATE", "UTC_TIME", "SOURCE", "START_TYPE", "END_TYPE", "ITEM", "TITLE", "TYPE_MATERIAL", "COMMENTS", "BREAK_RLYS", "SEGMENT", "DURATION", "TEXTOUT1", "PROGRAM_CLASS", "AUDIO_MODE_1", "EVENT_TYPE", "EVENT_NUM", "CUE_COUNTDOWN", "RELEASED", "SOURCE", "UNIQUE_EVENT_ID", "TONE_PROG_ID", "AFFILIATE_BREAK_RLYS", "BREAK_RLYS_3", "TONE_SPLICE_ID"], "subsidiary": [{"key": {"type": "Protection"}, "value":["SRC"]}]}}'
    logWriter("Fields configuration = [%s]" % body, False)

    logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    #print("    Params = [%s]" % str(params))

    eventFieldsResponse = requests.put(url, params=params, headers=headers, data=body)
    logWriter("Event Fields Status Code = [%s]" % str(eventFieldsResponse.status_code), False)
    #print("    Event Fields Content = [%s]" % eventFieldsResponse.content)
    eventFieldsResponseBody = eventFieldsResponse.text
    logWriter("Event Fields Response Body = [%s]" % eventFieldsResponseBody, False)
    eventFieldsResponseParsed = json.loads(eventFieldsResponseBody)

    return eventFieldsResponseParsed


def getTime(sessionId):
    logWriter("Getting the current system time", False)
    url = dServicesEndoint + "sessions/" + sessionId + "/time"
    logWriter("D-Services URL = [%s]" % url, False)

    getTimeResponse = requests.get(url)
    logWriter("Get Time Status Code = [%s]" % str(getTimeResponse.status_code), False)
    getTimeResponseBody = getTimeResponse.text
    if str(getTimeResponse.status_code) != "200":
        logWriter("Get Time Response Body = [%s]" % getTimeResponseBody, False)
    getTimeResponseParsed = json.loads(getTimeResponseBody)

    return getTimeResponseParsed['time']['time point']


def displayOnAirEvent():
    logWriter("Get the On-Air Event", True)

    eventId = getOnAirEvent(sessionId, busId)['event']['id']

    onAirEventData = getAnEvent(sessionId, busId, eventId)

    logWriter("onAirEventData = [%s]" % onAirEventData, False)

    currentServerTime = getTime(sessionId)
    currentTime = datetime.datetime.fromisoformat(currentServerTime)

    eventUTC_DATE = (onAirEventData['data']['primary']['UTC_DATE'] + "          ")[:10]
    eventUTC_TIME = onAirEventData['data']['primary']['UTC_TIME']
    eventSOURCE = (onAirEventData['data']['primary']['SOURCE'] + "        ")[:8]
    eventITEM = (onAirEventData['data']['primary']['ITEM'] + "                                ")[:32]
    eventTYPE_MATERIAL = (onAirEventData['data']['primary']['TYPE_MATERIAL'] + " ")[:1]
    eventSEGMENT = (onAirEventData['data']['primary']['SEGMENT'] + "  ")[:2]
    eventDURATION = onAirEventData['data']['primary']['DURATION']
    eventTITLE = (onAirEventData['data']['primary']['TITLE'] + "                                ")[:32]
    eventCOMMENTS = (onAirEventData['data']['primary']['COMMENTS'] + "                                ")[:32]

    eventCURRENT_TIME = str(currentTime.strftime("%H:%M:%S"))
    #print("  CURRENT_TIME (UTC) = [%s]" % eventCURRENT_TIME)

    #eventCURRENT_TIMEfr = (int(eventCURRENT_TIME[0:2]) * 90000) + (int(eventCURRENT_TIME[3:5]) * 1500) + (int(eventCURRENT_TIME[6:8]) * 25) + tzOffset
    #print("  CURRENT_TIME fr (local) = [%s]" % eventCURRENT_TIMEfr)
    eventCURRENT_TIMEfr = timeToFrames(eventCURRENT_TIME)
    #print("  CURRENT_TIME fr (original) = [%s]" % eventCURRENT_TIMEfr[0])
    #print("  CURRENT_TIME fr (local) = [%s]" % eventCURRENT_TIMEfr[1])

    eventCURRENT_TIME = framesToTime(eventCURRENT_TIMEfr[1])
    #print("  CURRENT_TIME (local) = [%s]" % eventCURRENT_TIME)

    # for the on-air event the UTC_TIME is the END_TIME
    #print("  eventUTC_TIME (UTC) = [%s]" % eventUTC_TIME)
    #eventUTC_TIMEfr = (int(eventUTC_TIME[0:2]) * 90000) + (int(eventUTC_TIME[3:5]) * 1500) + (int(eventUTC_TIME[6:8]) * 25) + tzOffset
    if not eventUTC_TIME == "":
        eventUTC_TIMEfr = timeToFrames(eventUTC_TIME)[1]
        eventEND_TIME = framesToTime(eventUTC_TIMEfr)
    else:
        eventUTC_TIMEfr = eventCURRENT_TIMEfr
        eventEND_TIME = str(eventCURRENT_TIMEfr)
    #print("  eventEND_TIME (local) = [%s]" % eventEND_TIME)

    if not eventDURATION == ":  :  :" and not eventDURATION == "**:**:**:**":
        #eventDURATIONfr = (int(eventDURATION[0:2]) * 90000) + (int(eventDURATION[3:5]) * 1500) + (int(eventDURATION[6:8]) * 25) + (int(eventDURATION[9:11]))
        eventDURATIONfr = timeToFrames(eventDURATION)[0]
        #print(eventDURATIONfr)

        eventCOUNTDOWNfr = eventUTC_TIMEfr - eventCURRENT_TIMEfr[1]
        eventCOUNTDOWN = framesToTime(eventCOUNTDOWNfr)
    else:
        eventDURATION = "  :  :  :  "
        eventCOUNTDOWN = "  :  :  "


    logWriter("  | DATE       | TIME     | DURATION    | SOURCE   | ITEM                             | TYPE | SEG |", True)
    logWriter("  | " + eventUTC_DATE + " | " + eventCURRENT_TIME + " | " + eventDURATION + " | " + eventSOURCE + " | " + eventITEM + " | " + eventTYPE_MATERIAL + "    | " + eventSEGMENT + "  |", True)
    logWriter("  ", True)

    logWriter("  |            | END TIME | COUNTDOWN   | TITLE                            | COMMENTS                         |", True)
    logWriter("  |            | " + eventEND_TIME + " | " + eventCOUNTDOWN + "    | " + eventTITLE + " | " + eventCOMMENTS + " |", True)
    logWriter("  ", True)


def getCacheList(sessionId, filter, cacheNumber):
    logWriter("Get the cache list wih filter [%s]" % filter, True)

    if filter == "Missing":
        filterNumber = "6"
    elif filter == "Surplus":
        filterNumber = "7"
    elif filter == "Scheduled":
        filterNumber = "8"
    else:
        filterNumber = "0"

    if cacheNumber == None:
        cacheNumber = 0

    url = dServicesEndoint + "caches/" + str(cacheNumber)  + "/filters/" + filterNumber
    logWriter("D-Services URL = [%s]" % url, True)

    headers = {'Content-Type': 'application/json'}

    params = {
        'session': sessionId
    }

    logWriter("Params = [%s]" % str(params), False)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    cacheResponse = requests.get(url, params=params, headers=headers)
    logWriter("Cache Status Code = [%s]" % str(cacheResponse.status_code), False)
    cacheResponseBody = cacheResponse.text
    logWriter("Cache Response Body = [%s]" % cacheResponseBody, False)
    cacheResponseParsed = json.loads(cacheResponseBody)

    return cacheResponseParsed

########################################################################################################################################################################################################
# functions end
########################################################################################################################################################################################################

# get execution variables from the parent script or command line
parser = argparse.ArgumentParser(description='D-Services test script')
parser.add_argument("-e", "--endpoint", help="D-Services Endpoint", required=True)
parser.add_argument("-m", "--mode", help="What to query", required=True)
parser.add_argument("-b", "--bus", help="Bus to query", required=False)
parser.add_argument("-l", "--loop", help="Loop time in seconds", required=False)
parser.add_argument("-c", "--cache", help="Cache number", required=False)
args = parser.parse_args()

dServicesEndointName = str(args.endpoint).upper()

cacheNumber = args.cache

fieldList = "NEW"
match dServicesEndointName:
    case "NPCA1":
        dServicesEndointIP = "10.50.222.17"
    case "NPCA2":
        dServicesEndointIP = "10.50.109.88"
    case "NPCB1":
        dServicesEndointIP = "10.50.109.21"
    case "NPCB2":
        dServicesEndointIP = "10.50.109.22"
    case "NPCC1":
        dServicesEndointIP = "10.50.227.17"
        fieldList = "OLD"
    case "NPCC2":
        dServicesEndointIP = "10.50.109.108"
        fieldList = "OLD"
    case "TBSA1":
        dServicesEndointIP = "10.51.109.87"
    case "TBSA2":
        dServicesEndointIP = "10.51.109.88"
    case "TBSB1":
        dServicesEndointIP = "10.51.109.21"
    case "TBSB2":
        dServicesEndointIP = "10.51.109.22"
    case "TBSC1":
        dServicesEndointIP = "10.51.109.107"
        fieldList = "OLD"
    case "TBSC2":
        dServicesEndointIP = "10.51.109.108"
        fieldList = "OLD"
    case _:
        #dServicesEndointIP = "10.50.109.185"        # Test system
        dServicesEndointIP = "10.12.70.226"        # Test system

dServicesEndoint = "http://" + dServicesEndointIP + ":60000/test/"

dServicesUsername = "dservices"
dServicesPassword = "dservices"

queryMode = str(args.mode).upper()

getCache = False
getonAirEvent = True
getPlaylist = False
getAsRunLog = False
createBusList = False
busId = False
filter = ""

match queryMode:
    case "CACHE":
        getCache = True
        filter = "None"
    case "CACHE-MISSING":
        getCache = True
        filter = "Missing"
    case "CACHE-SURPLUS":
        getCache = True
        filter = "Surplus"
    case "CACHE-SCHEDULED":
        getCache = True
        filter = "Scheduled"
    case "SCHEDULE":
        getPlaylist = True
    case "ASRUN":
        getAsRunLog = True
    case "BUSLIST":
        createBusList = True
    case _:
        pass

if getCache == False:
    busName = str(args.bus).upper()

    if busName == "NONE":
        logWriter("User did not specify a bus to query", False)
    else:
        busId = busName2Number(dServicesEndointName, busName)
        print(f"+++{busId}++++")

loopTime = str(args.loop)
if loopTime == "None":
    loopTime = 1000
    runOnlyOnce = True
else:
    runOnlyOnce = False

print("\n  D-Services Testing")
logWriter("D-Services Endoint Name = [%s]" % dServicesEndointName, True)
logWriter("D-Services Endoint URL = [%s]" % dServicesEndoint, True)
logWriter("Output Path = [%s]" % outputPath, False)
logWriter("Logging Path = [%s]" % logPath, False)
logWriter("Query Mode = [%s]" % queryMode, False)
if busId != False:
    logWriter("Bus ID = [%s]" % busId, False)
logWriter("Run Once = [%s]" % runOnlyOnce, False)
if runOnlyOnce == False:
    logWriter("Loop Time = [%s]" % loopTime, False)
print("  ")

print("  Initialise a new session")
sessionId = initSession()
logWriter("Session ID = [%s]\n" % sessionId, True)
#print("    Session ID = [%s]" % sessionId)
#print("  ")


print("  Get current system time")
serverTime = getTime(sessionId)
logWriter("System time = [%s]\n" % serverTime, True)
#print("    Time = [%s]" % serverTime)
#print("  ")
if filter == "":
    logWriter("Cache filter is blank so must be a schedule or as-run query\n" % filter, True)
    #print("  Configure desired event fields")
    fields = selectEventFields(sessionId)
    #print(fields)
    #print("  ")
else:
    logWriter("Cache filter is [%s] so not sending get event fields\n" % filter, True)


#createBusList = False

if createBusList == True:

    print("  Get bus list")
    busList = getBuses(sessionId)['buses']
    #print("  Buses = [%s]" % busList)
    #print("  ")

    #print("  Bus #, Name, Description")
    #busListText = "Bus #, Name, Description, Flags\n"
    busListText = "Bus #, Name, Description\n"

    #altBuses = ""

    for busId in busList:

        busConfig = getBusConfig(sessionId, busId)

        #if not str(busConfig['name']) in str(altBuses):
        if busConfig['flags'] == "128":
            #print("  [%s], [%s], [%s]" % (str(busId), busConfig['name'], busConfig['description']))
            #busListText += ("000" + str(busId))[-3:] + ", " + (busConfig['name'] + "        ")[:8] + ", " + (busConfig['description'] + "                    ")[:20] + ", " + busConfig['flags'] + ", " + bin(int(busConfig['flags'])) + "\n"
            busListText += ("000" + str(busId))[-3:] + ", " + (busConfig['name'] + "        ")[:8] + ", " + (busConfig['description'] + "                    ")[:20] + "\n"

        elif busConfig['flags'] == "177":
            if re.search("KEEP", busConfig['name']):

                busListText += ("000" + str(busId))[-3:] + ", " + (busConfig['name'] + "        ")[:8] + ", " + (busConfig['description'] + "                    ")[:20] + "\n"

        #altBuses += str(busConfig['name']) + ", "

    busListFile = open(outputPath + dServicesEndointIP + "_bus-list.txt", "w")
    busListFile.write(busListText + "\n")
    busListFile.close()

    print("  Bus list written to file [%s]" % outputPath + "bus-list.txt")
    print("  ")

    #busConfig = getBusConfig(sessionId, "100")

    #print("  Bus Name = [%s]" % busConfig['name'])
    #print("  Bus Description = [%s]" % busConfig['description'])

    #busConfig = getBusConfig(sessionId, "302")

    #print("  Bus Name = [%s]" % busConfig['name'])
    #print("  Bus Description = [%s]" % busConfig['description'])

    #busConfig = getBusConfig(sessionId, "305")

    #print("  Bus Name = [%s]" % busConfig['name'])
    #print("  Bus Description = [%s]" % busConfig['description'])
    #print("  ")

#getPlaylist = False
#getonAirEvent = False
#runOnlyOnce = True

if getPlaylist == True:
    try:
        while True:
            busConfig = getBusConfig(sessionId, busId)
            eventBUS = (busConfig['name'] + "        ")[:8]
            print("  Events Bus = [%s]" % eventBUS)
            if getonAirEvent == True:
                displayOnAirEvent()
            print("  Get Playlist")
            scheduleList = getEvents(sessionId, busId, False)['events']
            #print("  Events = [%s]" % scheduleList)
            #print("  ")
            print("  Bus     , Date UTC  , Time UTC   , Local   , Source  ,Item                    ,Type,Seg, Duration   , Title                           , Comments")
            counter = 1
            for event in scheduleList:
                for key, value in event.items():
                    match key:
                        case "id":
                            eventId = value
                        case _:
                            pass
                eventData = getAnEvent(sessionId, busId, eventId)
                #print(eventData)
                eventEVENT_TYPE = eventData['data']['primary']['EVENT_TYPE']
                eventUTC_DATE = eventData['data']['primary']['UTC_DATE']
                eventUTC_TIME = eventData['data']['primary']['UTC_TIME']
                eventSOURCE = (eventData['data']['primary']['SOURCE'] + "        ")[:8]
                eventITEM = (eventData['data']['primary']['ITEM'] + "                                ")[:24]
                eventTYPE_MATERIAL = (eventData['data']['primary']['TYPE_MATERIAL'] + "    ")[:4]
                eventSEGMENT = (eventData['data']['primary']['SEGMENT'] + "   ")[:3]
                eventDURATION = eventData['data']['primary']['DURATION']
                if eventDURATION == ":  :  :":
                    eventDURATION = "  :  :  :  "
                eventTITLE = (eventData['data']['primary']['TITLE'] + "                                ")[:32]
                eventCOMMENTS = (eventData['data']['primary']['COMMENTS'] + "                                                                ")[:64]

                eventSTART_TIMEfr = timeToFrames(eventUTC_TIME)[1]
                eventSTART_TIME = framesToTime(eventSTART_TIMEfr)

                if eventEVENT_TYPE == "C":
                    print("  %s, %s, %s, %s,--------------------------------------------------------, COMMENT - %s" % (eventBUS, eventUTC_DATE, (eventUTC_TIME + "           ")[:11], eventSTART_TIME, eventTITLE))
                else:
                    print("  %s, %s, %s, %s, %s,%s,%s,%s, %s, %s, %s" % (eventBUS, eventUTC_DATE, (eventUTC_TIME + "           ")[:11], eventSTART_TIME, eventSOURCE, eventITEM, eventTYPE_MATERIAL, eventSEGMENT, eventDURATION, eventTITLE, eventCOMMENTS))

                counter += 1
                # not needed as the 'schedule window' in the session creation sets this limit
                #if counter > 1000:
                #    break

            if runOnlyOnce == True:
                break
            else:
                serverTime = getTime(sessionId)
                logWriter("Query finished [%s] in session [%s]" % (serverTime, sessionId), True)
                logWriter("------------------------------------------------------------", False)

            print("\nPress CTRL+C to exit\n")

            #time.sleep(int(loopTime))
            for remaining in range(int(loopTime), 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write("  {:2d} seconds remaining  ".format(remaining))
                sys.stdout.flush()
                time.sleep(1)

    except KeyboardInterrupt:
        pass
        print("\nQuit by user keystroke")

#getAsRunLog = False
#runOnlyOnce = True

if getAsRunLog == True:
    try:
        while True:
            eventsList = []
            busConfig = getBusConfig(sessionId, busId)
            eventBUS = busConfig['name']
            displayOnAirEvent()

            print("  Get As-Run Log")
            asRunList = getEvents(sessionId, busId, True)['events']
            #print("  Events = [%s]" % scheduleList)
            #print("  ")
            counter = 1
            logWriter("  Bus     , Date UTC  , Time UTC   , Local   , Source  ,Item                    ,Type,Seg, Duration   , Title                         , Comments                      ,Brk,Aff,3rd,ProgID,Splice,EventID", True)
            for event in asRunList:
                for key, value in event.items():
                    match key:
                        case "id":
                            eventId = value
                        case _:
                            pass
                eventData = getAnEvent(sessionId, busId, eventId)

                if eventData == 404:
                    logWriter("ERROR - getAnEvent returned code 404 - event has probably been deleted since the event list was returned", False)

                    #Error condition/status codes, may be found in the D-Services log:
                    #    1 (kArguments)     = 200 OK
                    #   11 (kInternalError) = 500 Internal Server Error
                    #   12 (kProtocolError) = 400 Bad Request
                    #   21 (kUnauthorized)  = 403 Forbidden
                    #   22 (kNotFound)      = 404 Not found
                    #   23 (kConflict)      = 409 Conflict

                else:
                    eventEVENT_TYPE = eventData['data']['primary']['EVENT_TYPE']
                    eventUTC_DATE = eventData['data']['primary']['UTC_DATE']
                    eventUTC_TIME = eventData['data']['primary']['UTC_TIME']
                    eventTYPE_MATERIAL = (eventData['data']['primary']['TYPE_MATERIAL'] + "   ")[:3]
                    eventSEGMENT = (eventData['data']['primary']['SEGMENT'] + "   ")[:3]
                    eventSOURCE = (eventData['data']['primary']['SOURCE'] + "        ")[:8]
                    eventITEM = (eventData['data']['primary']['ITEM'] + "                                ")[:24]
                    eventDURATION = eventData['data']['primary']['DURATION']
                    if eventDURATION == ":  :  :":
                        eventDURATION = "  :  :  :  "
                    eventTITLE = (eventData['data']['primary']['TITLE'] + "                                ")[:30]
                    eventCOMMENTS = (eventData['data']['primary']['COMMENTS'] + "                                                                ")[:30]
                    eventTONE_PROG_ID = eventData['data']['primary']['TONE_PROG_ID']
                    eventTONE_SPLICE_ID = eventData['data']['primary']['TONE_SPLICE_ID']
                    eventBREAK_RLYS = (eventData['data']['primary']['BREAK_RLYS'] + "   ")[:3]
                    eventAFFILIATE_BREAK_RLYS = (eventData['data']['primary']['AFFILIATE_BREAK_RLYS'] + "   ")[:3]
                    eventBREAK_RLYS_3 = (eventData['data']['primary']['BREAK_RLYS_3'] + "   ")[:3]

                    eventSTART_TIME = eventUTC_TIME
                    #eventSTART_TIMEfr = (int(eventSTART_TIME[0:2]) * 90000) + (int(eventSTART_TIME[3:5]) * 1500) + (int(eventSTART_TIME[6:8]) * 25) + tzOffset
                    eventSTART_TIMEfr = timeToFrames(eventSTART_TIME)[1]
                    eventSTART_TIME = framesToTime(eventSTART_TIMEfr)

                    #print("  %s, %s, %s, %s, %s, %s, %s" % (eventBUS, eventUTC_DATE, eventUTC_TIME, eventSOURCE, eventITEM, eventDURATION, eventTITLE))

#                    eventsList.append(eventBUS + "," + eventUTC_DATE + "," + eventUTC_TIME + "," + eventSOURCE + "," + eventITEM + "," + eventTYPE_MATERIAL + "," + eventSEGMENT + "," + eventDURATION + "," + eventTITLE + "," + eventCOMMENTS + "," + eventId + "," + eventTONE_PROG_ID + "," + eventBREAK_RLYS + "," + eventAFFILIATE_BREAK_RLYS + "," + eventTONE_SPLICE_ID)

#                   logWriter("  Bus     , Date UTC  , Time UTC, Local   , Source  ,Item                            ,Type,Seg, Duration   , Title                         , Comments                      ,Brk,Aff,ProgID,Splice,EventID", True)

                    if eventEVENT_TYPE == "C":
                        logWriter("  " + (eventBUS + "        ")[:8] + ", " + eventUTC_DATE + ", " + (eventUTC_TIME + "           ")[:11] + ", " + eventSTART_TIME + ",--------------------------------------------------------, COMMENT - " + eventTITLE, True)
                    else:
                        logWriter("  " + (eventBUS + "        ")[:8] + ", " + eventUTC_DATE + ", " + (eventUTC_TIME + "           ")[:11] + ", " + eventSTART_TIME + ", " + eventSOURCE + "," + eventITEM + ", " + eventTYPE_MATERIAL + "," + eventSEGMENT + ", " + eventDURATION + ", " + eventTITLE + ", " + eventCOMMENTS + "," + eventBREAK_RLYS + "," + eventAFFILIATE_BREAK_RLYS + "," + eventBREAK_RLYS_3 + "," + (eventTONE_PROG_ID + "        ")[:6] + "," + (eventTONE_SPLICE_ID + "        ")[:6] + "," + eventId, True)


#            logWriter("Sorting As-Run log to display only the most recent events", False)
#            eventsList.sort(reverse=True)
#
#            counter = 1
#
#            logWriter("  Bus     , Date UTC  , Time UTC, Local   , Source  ,Item                            ,Type,Seg, Duration   , Title                         , Comments                      ,Brk,Aff,ProgID,Splice,EventID", True)
#
#            for event in eventsList:
#
#                #print(event)
#                eventSplit = event.split(",")
#
#                eventSTART_TIME = eventSplit[2]
#                #eventSTART_TIMEfr = (int(eventSTART_TIME[0:2]) * 90000) + (int(eventSTART_TIME[3:5]) * 1500) + (int(eventSTART_TIME[6:8]) * 25) + tzOffset
#                eventSTART_TIMEfr = timeToFrames(eventSTART_TIME)[1]
#                eventSTART_TIME = framesToTime(eventSTART_TIMEfr)
#
#                #print("  " + (eventSplit[0] + "        ")[:8] + ", " + eventSplit[1] + ", " + eventSplit[2] + ", " + eventSTART_TIME + ", " + (eventSplit[3] + "        ")[:8] + "," + (eventSplit[4] + "                                ")[:32] + "," + (eventSplit[5] + "    ")[:4] + "," + (eventSplit[6] + "   ")[:3] + ", " + eventSplit[7] + ", " + (eventSplit[8] + "                                ")[:32] + ", " + (eventSplit[9] + "                                ")[:32]+ "," + eventSplit[10])
#                #print("  " + (eventSplit[0] + "        ")[:8] + ", " + eventSplit[1] + ", " + eventSplit[2] + ", " + eventSTART_TIME + ", " + (eventSplit[3] + "        ")[:8] + "," + (eventSplit[4] + "                                ")[:32] + "," + (eventSplit[5] + "    ")[:4] + "," + (eventSplit[6] + "   ")[:3] + ", " + eventSplit[7] + ", " + (eventSplit[8] + "                                ")[:32] + ", " + (eventSplit[9] + "                                ")[:32] + "," + (eventSplit[12] + "   ")[:3] + "," + (eventSplit[13] + "   ")[:3] + "," + (eventSplit[11] + "        ")[:8] + "," + eventSplit[14])
#                logWriter("  " + (eventSplit[0] + "        ")[:8] + ", " + eventSplit[1] + ", " + eventSplit[2] + ", " + eventSTART_TIME + ", " + (eventSplit[3] + "        ")[:8] + "," + (eventSplit[4] + "                                ")[:32] + "," + (eventSplit[5] + "    ")[:4] + "," + (eventSplit[6] + "   ")[:3] + ", " + eventSplit[7] + ", " + (eventSplit[8] + "                                ")[:30] + ", " + (eventSplit[9] + "                                ")[:30] + "," + (eventSplit[12] + "   ")[:3] + "," + (eventSplit[13] + "   ")[:3] + "," + (eventSplit[11] + "        ")[:6] + "," + (eventSplit[14] + "        ")[:6] + "," + eventSplit[10], True)


                counter += 1
                # not needed as the 'as-run window' in the session creation sets this limit
                #if counter > 20:
                #    break

            if runOnlyOnce == True:
                break
            else:
                serverTime = getTime(sessionId)
                logWriter("Query finished [%s] in session [%s]" % (serverTime, sessionId), True)
                logWriter("------------------------------------------------------------", False)

            print("\nPress CTRL+C to exit\n")

            #time.sleep(int(loopTime))
            for remaining in range(int(loopTime), 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write("  {:2d} seconds remaining  ".format(remaining))
                sys.stdout.flush()
                time.sleep(1)

    except KeyboardInterrupt:
        pass
        print("\nQuit by user keystroke")




#getCache = True
#runOnlyOnce = False

if getCache == True:
    try:
        while True:
            print("\n  Get Cache [%s] List" % (filter))
            try:
                cacheList = getCacheList(sessionId, filter, cacheNumber)['cache list']
                counter = 0
                logWriter("  Avail,  Date  ,  Time  ,Schedule, Material                        , Duration  , Title", True)
                for material in cacheList:
                    materialTitle = "                                     [TITLE and ABTITLE are blank]"
                    print(f"=={material}===")
                    for key, value in material.items():
                        match key:
                            case "Av":
                                materialAvail = value
                            case "Date":
                                materialDate = value
                            case "Time":
                                materialTime = value
                            case "Sched":
                                materialSched = value
                            case "Material ID":
                                materialID = value
                            case "Duration":
                                materialDuration = value
                            case "AbbTitle":
                                materialTitle = value
                            case "Event Title":
                                materialTitle = value
                            case _:
                                pass
                    counter += 1
                    if counter < 25:
                        logWriter("  " + (materialAvail + "     ")[:5] + "," + materialDate + "," + materialTime + "," + (materialSched + "        ")[:8] + ", " + (materialID + "                                ")[:32] + "," + materialDuration + ", " + materialTitle, True)
                    elif counter < 26:
                        print("  ..and more clips")
                    else:
                        pass
                logWriter("There are [%s] [%s] items" % (counter, filter), True)
            except KeyError as err:
                logWriter("Could not get cache [%s] for session [%s]. System returned an error:  check log for details" % (filter, sessionId), True)
            if runOnlyOnce == True:
                break
            else:
                serverTime = getTime(sessionId)
                logWriter("Query finished [%s] in session [%s]" % (serverTime, sessionId), True)
                logWriter("------------------------------------------------------------", False)
            print("\nPress CTRL+C to exit\n")
            #time.sleep(int(loopTime))
            for remaining in range(int(loopTime), 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write("  {:2d} seconds remaining  ".format(remaining))
                sys.stdout.flush()
                time.sleep(1)

    except KeyboardInterrupt:
        pass
        print("\nQuit by user keystroke")

#print("  Ping an existing session")
#ping = pingSession(sessionId)
#print("  Ping = [%s]\n" % ping)

print("  Delete the session")
delete = deleteSession(sessionId)
#print("  Delete = [%s]\n" % delete)