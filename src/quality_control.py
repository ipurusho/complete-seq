#!/usr/bin/python
from utils import *
import re
import pysam
import os
import csv
import subprocess

shell_splitUniqe = "|cut -f1|sort -u |wc -l" #shell command to count unique reads only

######## temp variables #####################################
exonicPath = "/home/immanuel/Desktop/mm9_bed/exon.bed"
intronicPath = "/home/immanuel/Desktop/mm9_bed/intron.bed"
intragenicPath = "/home/immanuel/Desktop/mm9_bed/intragenic.bed"
intergenicPath = "/home/immanuel/Desktop/mm9_bed/intragenic.bed"
totalReads = 51164922.0
#############################################################

class GetReads(object):
	def __init__(self,dir): #pass directory to this class
		self.dir = dir
		
	def totalReads(self): #figure out how to execute this class properly
		def tophatTotal(self): #get and return reads in (single and paired) from output file
		#support single and paired
			#getReadsIn = Utility() 
			#counts = getReadsIn.openFile(self.dir,"prep_reads.info")
			print "yo"
			
	def mappedTotal(self): #support all alignment outputs  in future
		command = "samtools view "+self.dir+"/accepted_hits.bam " + shell_splitUniqe
		mappedReads = subprocess.check_output(command, shell=True)
		return mappedReads
	#individual mapping rates
	def intragenic(self): 
		command = "samtools view "+self.dir+"/accepted_hits.bam -L "+ intragenicPath + " " + shell_splitUniqe
		intragenic = subprocess.check_output(command, shell=True)
		return intragenic
	
	def exon(self):
		command = "samtools view "+self.dir+"/accepted_hits.bam -L "+ exonicPath + " " + shell_splitUniqe
		exon = subprocess.check_output(command, shell=True)
		return exon
	
	def intron(self):
		command = "samtools view "+self.dir+"/accepted_hits.bam -L "+ intronicPath + " " + shell_splitUniqe
		intron = subprocess.check_output(command, shell=True)
		return intron
	
	def intergenic(self):
		command = "samtools view "+self.dir+"/accepted_hits.bam -L "+ intergenicPath + " " + shell_splitUniqe
		intergenic = subprocess.check_output(command, shell=True)
		return intergenic
	
	def mitochondrial(self):
		mitochondrial = pysam.Samfile(self.dir+"/accepted_hits.bam", "rb" ).count(region='MT')
		return mitochondrial
	
	def ribosomal(self):
		#might require a bowtie or downsampled bwa alignment
		pass

class QCReport(object):
	
	def __init__(self,dir): #pass directory to this class
		
		self.dir = dir
		self.rawReads = GetReads(dir)
	
	#@dd decorator
	def gatherReport(self): #computes rates 
		mapping = self.rawReads.mitochondrial()  / totalReads
		intragenic = self.rawReads.intragenic()/rawReads.mappedTotal()
		exonic = self.rawReads.exon()/rawReads.mappedTotal()
		intronic = self.rawReads.intron()/rawReads.mappedTotal()
		intergenic = self.rawReads.intergenic()/rawReads.mappedTotal()
		chrMTrate = self.rawReads.mitochondrial()/rawReads.mappedTotal()
		#concatenates rates in a tab-delimted string
		## change name to pass sample name to method
		sample = "Name" + "\t" + str(mapping) +"\t"+ str(intragenic)+ "\t" + str(exonic) + "\t" + str(intronic) + "\t"+ str(intragenic) + "\t" + str(chrMTrate) + "\n"
		return sample
	
	def writeReport(self):
		file = open("sample.txt", "w")
		file.write(self.gatherReport())
		file.close()
		
	def testReport(self):
		print "Testing if python class is launched from specific script"
# test = QCReport("/home/immanuel/Documents/Sample_project/mapping/CPU_C4_ACTTGA_L005_R1_001.tophat2")
# test.testReport()