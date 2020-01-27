#created using Python 3.7.3

import sys
import queue

filename = "jugglefest.txt"
circuits = {}
jugglers = queue.LifoQueue()

# circuit attributes

# parse Circuit's Id including the 'C' prefix
# returns String
def cid_full(str):
	start = str.index('C', 1)
	end = str.index(' ', start)
	return str[start:end]

# parse Circuit's Id excluding the 'C' prefix
# returns integer
def cId(str):
	start = str.index('C', 1) + 1
	end = str.index(' ', start)
	return int(str[start:end])

# parse Circuit's Hand-To-Eye Coordination
# returns integer
def cH(str):
	start = str.index('H:') + 2
	end = str.index(' ', start)
	return int(str[start:end])

# parse Circuit's Endurance
# returns integer
def cE(str):
	start = str.index('E:') + 2
	end = str.index(' ', start)
	return int(str[start:end])

# parse Circuit's Pizzazz
# returns integer
def cP(str):
	start = str.index('P:') + 2
	return int(str[start:])

# juggler attributes

# parse Juggler's Id including the 'J' prefix 
# returns string
def jid_full(str):
	start = str.index('J', 1)
	end = str.index(' ', start)
	return str[start:end]

# parse Juggler's Id excluding the 'J' prefix
# returns integer
def jId(str):
	start = str.index('J', 1) + 1
	end = str.index(' ', start)
	return int(str[start:end])

# parse Juggler's Hand-To-Eye Coordination
# returns integer
def jH(str):
	start = str.index('H:') + 2
	end = str.index(' ', start)
	return int(str[start:end])

# parse Juggler's Endurance
# returns integer
def jE(str):
	start = str.index('E:') + 2
	end = str.index(' ', start)
	return int(str[start:end])

# parse Juggler's Pizzazz
# returns integer
def jP(str):
	start = str.index('P:') + 2
	end = str.index(' ', start)
	return int(str[start:end])

# parse Juggler's Preferences
# returns string
def jPrefs(str):
	start = str.index('C')
	return str[start:]

# parse Circuit Id of Juggler Preference
# return integer
def jPrefId(str):
	start = str.index('C') + 1
	return int(str[start:])

# parse String-Array of Juggler Preferences
# returns String[]
def jPrefsArray(str):
	return jPrefs(str).split(',')

# calculate dot-product of Circuit and Juggler
# returns integer
def dot_product(c,j):
	return cH(c)*jH(j)\
			+ cE(c)*jE(j)\
			+ cP(c)*jP(j)

def matchh(j,c):
	cdata = c['data']
	cmembers = c['members']
	cid = cid_full(cdata)
	#does the circuit have room for the juggler
	jid = jid_full(j)
	jdp = dot_product(cdata,j)

	print('')
	print('?' + jid + ':'+ str(jdp) +' =>' + cdata)
	if len(cmembers) < group_size:
		#add juggler
		cmembers.append(j)
		#print action description
		print(cdata)
		output = '\t'
		for jm in cmembers:
			output = output + jid_full(jm) + ' '
		print(output)
		print('\t' + jid +' !accepted')
	else :
		#print action description
		print(cdata)
		output = '\t'
		for jm in cmembers:
			mdp = dot_product(cdata,jm)
			output = output + jid_full(jm) + ':' + str(mdp) + ' '
		print(output)

		#find the weakest juggler match in circuit by dot product
		min_dp = sys.maxsize
		min_j = ''
		for jm in cmembers :
			mdp = dot_product(cdata, jm)
			if mdp < min_dp :
				min_dp = mdp
				min_j = jm
		#if the returned min_dp is less than the requested joiner swap jugglers
		if jdp > min_dp :
			cmembers.remove(min_j)
			cmembers.append(j)
			#print action description

			mid_start = min_j.index('J', 1)
			mid_end = min_j.index(' ', mid_start)

			print('\t' + jid +' !accepted')
			print('\t' + jid_full(min_j) + '<' + ' ' + jid +'>')

			cidToend_start = min_j.index(cid)
			min_j = min_j[:cidToend_start + 1] + '-' + min_j[cidToend_start + 1:]
			print(min_j)
			jugglers.put(min_j)
			#match(min_j,min_jprefs)
		else :
			#mark the preference as having a negative number
			#prefs.remove(prefs[0])
			print('\t' + jid + ' !rejected')
			cidToend_start = j.index(cid)
			j = j[:cidToend_start + 1] + '-' + j[cidToend_start + 1:]
			print(j)
			jugglers.put(j)
			#match(j,prefs,group_size)

def match(j,prefs):
	if(len(prefs)==0):
		print(j , ' leads to instability')
		sys.exit()
	#next preference
	c = circuits[jPrefId(prefs[0])]
	#does the circuit have room for the juggler
	jid_start = j.index('J', 1)
	jid_end = j.index(' ', jid_start)
	print('')
	print('?' + j[jid_start:jid_end] + ':'+ str(dot_product(c['data'],j)) +' =>' + c['data'])
	if len(c['members']) < group_size:
		#add juggler
		c['members'].append(j)
		#print action description
		print(c['data'])
		output = '\t'
		for m in c['members']:
			mid_start = m.index('J', 1)
			mid_end = m.index(' ', mid_start)
			output = output + m[mid_start:mid_end] + ' '
		print(output)
		print('\t' + j[jid_start:jid_end]+' !accepted')
	else :
		#determine dot product
		dp = dot_product(c['data'],j)
		#print action description
		print(c['data'])
		output = '\t'
		for m in c['members']:
			mid_start = m.index('J', 1)
			mid_end = m.index(' ', mid_start)
			mdp = dot_product(c['data'],m)
			output = output + m[mid_start:mid_end] + ':' + str(mdp) + ' '
		print(output)

		#find the weakest juggler match in circuit by dot product
		min_dp = sys.maxsize
		min_j = ''
		for jm in c['members'] :
			mdp = dot_product(c['data'], jm)
			if mdp < min_dp :
				min_dp = mdp
				min_j = jm
		#if the returned min_dp is less than the requested joiner swap jugglers
		if dp > min_dp :
			c['members'].remove(min_j)
			c['members'].append(j)
			#place the removed juggler on their next preferred circuit
			min_jprefs = min_j[min_j.index(prefs[0]) + len(prefs[0]):]
			if min_jprefs[0] == ',':
				min_jprefs = min_jprefs[1:]
			min_jprefs = min_jprefs.split(',')

			#print action description
			mid_start = min_j.index('J', 1)
			mid_end = min_j.index(' ', mid_start)

			print('\t' + j[jid_start:jid_end]+' !accepted')
			print('\t' + min_j[mid_start:mid_end] + '<' + ' ' + j[jid_start:jid_end]+'>')
			cdata = c['data']
			cid_start = cdata.index('C', 1)
			cid_end = cline.index(' ', cid_start)
			cid = cdata[cid_start:cid_end]
			cidToend_start = min_j.index(cid)
			min_j = min_j[0:cidToend_start] + '-' + min_j[cidToend_start:]
			jugglers.put(min_j)
			#match(min_j,min_jprefs)
		else :
			#mark the preference as having a negative number
			#prefs.remove(prefs[0])
			print('\t' + j[jid_start:jid_end] + ' !rejected')
			cdata = c['data']
			cid_start = cdata.index('C', 1)
			cid_end = cline.index(' ', cid_start)
			cid = cdata[cid_start:cid_end]
			cidToend_start = j.index(cid)
			j = j[0:cidToend_start] + '-' + j[cidToend_start:]
			jugglers.put(j)
			print(j)
			#match(j,prefs,group_size)

def print_circuit(cmapping):
	output = ''
	# add circuit id
	cline = cmapping['data']
	cid_start = cline.index('C', 1)
	cid_end = cline.index(' ', cid_start)
	cId = cline[cid_start:cid_end]
	output = output + cId
	# add the juggler id for each juggler with their
	# preferences and the preference dot product
	for jm in cmapping['members']:
		#add juggler id
		jid_start = jm.index('J', 1)
		jid_end = jm.index(' ', jid_start)
		jId = jm[jid_start:jid_end]
		output = output + ' ' + jId	+ ' '
		for c in jPrefsArray(jm):
			cid = int(c[1:])
			dp = dot_product(circuits[cid]['data'],jm)
			output = output + c + ':' + str(dp)
			if jPrefsArray(jm).index(c) != len(jPrefsArray(jm))-1:
				output = output + ' '
		if cmapping['members'].index(jm) != len(cmapping['members'])-1:
			output = output + ','
	print(output)


# determine number of circuits and jugglers
total_circuits = 0
total_jugglers = 0

f = open(filename, "r")
for line in f.readlines():
	if line[0] == 'C':
		total_circuits = total_circuits + 1
	elif line[0] == 'J':
		total_jugglers = total_jugglers + 1
group_size = int(total_jugglers/total_circuits)

print( 'total circuits:', total_circuits)
print( 'total jugglers:', total_jugglers)
print( 'group size:', group_size)

f = open(filename, "r")
for line in f.readlines():
	line = line.rstrip()
	if len(line) > 0:
		if line[0] == 'C':
			circuits[cId(line)]={\
				"data" : line,\
				"members" : []}
		elif line[0] == 'J':
			matchh(line,circuits[int(jPrefsArray(line)[0][1:])])

#count = 0
#print('****************')
while jugglers.empty != True:
#	count = count + 1
	j = jugglers.get()
	#find next non-negative preference
	jprefs = jPrefsArray(j)
	print('****'+str(jPrefsArray(j)))

	next_pref = ''
        # find the next non-negative preference
	for pref in jprefs:
		#print('***'+str(jPrefsArray(j)))
		if int(pref[1:]) > 0:
			next_pref = pref[1:]
			break
		elif jprefs.index(pref) == len(jprefs)-1:
			#move to the next positive
			print('abended at ' + j)
			sys.exit()

        matchh(j,circuits[int(next_pref)])


#for c in circuits:
#	print_circuit(circuits, circuits[c])
