import PyPluMA

class DESeq2TXTPlugin:
    def input(self, filename):

      self.parameters = dict()
      paramfile = open(filename, 'r')
      for line in paramfile:
         contents = line.split('\t')
         self.parameters[contents[0]] = contents[1].strip()
      infile = open(PyPluMA.prefix()+"/"+self.parameters["taxa"], 'r')
      self.deseqfile = open(PyPluMA.prefix()+"/"+self.parameters["deseq"], 'r')

      firstline = infile.readline()
      self.taxa = firstline.strip().split(',')
      self.group1 = self.parameters["group1"]
      self.group2 = self.parameters["group2"]
      self.pvalue = float(self.parameters["pvalue"])

    def run(self):
        pass

    def output(self, filename):
      firstdeseq = self.deseqfile.readline()
      contents2 = firstdeseq.strip().split(',')
      idx = contents2.index("\"pvalue\"")
      idx2 = contents2.index("\"log2FoldChange\"")
      outfile = open(filename, 'w')
      outfile.write("Taxon\tGroup\tLogFoldChange\tPValue\n")
      listResults = []
      for line in self.deseqfile:
          contents = line.strip().split(',')
          if (contents[idx] != "NA"):
             pvalue = float(contents[idx])
             index = contents[0]
             index = index[1:len(index)-1]
             index = int(index)
             printstring = str(self.taxa[index])#+"\t"+str(contents[idx2])
             group = "0"
             if (float(contents[idx2]) < 0):
                    printstring += "\t"+self.group1
                    group = self.group1
             else:
                    printstring += "\t"+self.group2
                    group = self.group2
             printstring += "\t"+contents[idx2]
             printstring += "\t"+str(pvalue)
             if (pvalue <= self.pvalue):
                outfile.write(printstring+"\n")
             listResults.append((pvalue, self.taxa[index], group))
      listResults.sort()
      #print(listResults)
