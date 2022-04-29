#python merger_2.py cog-20.fa cog-20.cog.csv cog-20.def.tab

import sys, time, re


# Build the dictionary of GenBank protein ID to COG ID
cog_db = {}
t0 = time.time()

with open(sys.argv[2], "r") as cog_file:
  for line in cog_file:
    split = line.split(",")
    cog_db[split[2]] = split[6]
  t1 = time.time()

print(f"\nCog file read. Time elapsed: {t1-t0} seconds.")


# Build the dictionary of COG ID to COG functional category and COG name
trans_cog = {}

with open(sys.argv[3], "r", encoding="cp1252") as cog_trans_file:
  for line in cog_trans_file:
    split = line.split("\t")
    trans_cog[split[0]] = (split[1],split[2])


# Using the dictionary to write to the outfile the protein sequences with COG info
error_count = 0

with open(sys.argv[1], "r") as prot_file:
  with open("merged_cogs.fa", "w") as outfile:
    for line in prot_file:
      if line[0] == ">":
        gi_id = line.split(' ')[0][1:]
        edit_id = re.search('(\d_\d)',gi_id)
        if edit_id:
          old_id = gi_id
          gi_id = gi_id.replace(edit_id.group(1),edit_id.group(1).replace('_','.'))
          line = line.replace(old_id,gi_id)
        edit_id = False
        try:
          outfile.write(" | ".join([line.strip(),cog_db[gi_id],trans_cog[cog_db[gi_id]][0]])+"\n")
        except KeyError:
          error_count += 1
          outfile.write(line.strip()+" | NO COG FOUND | NA\n")
          continue
      else: outfile.write(line)

t2 = time.time()

print("Protein file analyzed. Time elapsed: " + str(t2-t1) + " seconds.")
print("Number of sequences without a COG: " + str(error_count) + "\n")
