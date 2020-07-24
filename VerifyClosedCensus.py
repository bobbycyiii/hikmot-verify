import snappy
import hikmot
print_data = 0
good = []
bad = []
corrections = 0
coverList = []
knownGoodCovers= ['ClosedManifolds/Closed3_cover.tri']
coverDegree = 3
remainingBadManifolds = []

print("You will probably fail proving Closed3.tri to be hyperbolic, this is 'm007(3,1)' and we need to take a cover for this manifold.")
for counter in range(11031):
#for counter in range(110):                                                                                                                                
    M = snappy.Manifold('ClosedManifolds/Closed' + str(counter+1) + '.tri')
    N = snappy.OrientableClosedCensus[counter]
    if hikmot.verify_hyperbolicity(M,print_data)[0] and M.is_isometric_to(N):
        good.append(counter)
    else:
        print("Failed proving the hyperbolicity of Closed" + str(counter+1) + ".tri aka " + str(M) + ".")
        bad.append(counter)
        coverList.append([M.covers(coverDegree),M])

# These few lines check the grammar of our print out.
if len(bad)==1:
    finalWord = " error."
else:
    finalWord = " errors."

print("Out of 11031 manifolds in OrientableClosedCensus," + str(len(good)) + " manifolds have been proven to be hyperbolic!   " + str(len(bad)) + finalWord)

# This procedure really just verifies the hyperbolicity of a 3 fold cover of m007(3,1) 
# however we present it in the following way so that it may be scaled for future users.
# The knownGoodCovers is a set of file names for known good triangulations of problem manifolds above.
# This file was created by Algorithm 2 of our paper.
# This section of the code shows that a 3 fold cover of m007(3,1) is isometric to a triangutation we
# can verify. It is the final step of our proof.                                                                                                           
for manList in coverList:
    badMan = manList[1]
    for c in knownGoodCovers:
        cMan = snappy.Manifold(c)
        if hikmot.verify_hyperbolicity(cMan,print_data)[0]:
            for M in manList[0]:
                if M.is_isometric_to(cMan):
                    corrections = corrections + 1
                    print("Verified the  hyperbolicity of " + str(M) + ", a cover of " + str(badMan) + ".")
                    break
                else:
                    print("Failed proving the hyperbolicity of " + str(M) + ", a cover of " + str(badMan) + ".")
                    localListIndex = localListIndex+1
                    if localListIndex == len(manList[0])-1:
                        remainingBadManifolds.append(badMan)

# These few lines check the grammar of our print out.
if len(bad)==1:
    howMany = "There was one bad manifold. It has "
else:
    howMany = "Out of " +str(len(bad)) + " manifolds " +  str(corrections) + " have "
                        
print(howMany + "been verified and " + str(len(remainingBadManifolds)) + " remain.")
