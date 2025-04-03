"""
File: voter_analytics/models.py
Author: Winson Dong (winson@bu.edu)
Description:
     Defines database models for Voter.
"""

from django.db import models

# Create your models here.

class Voter(models.Model):
    ''' model definition to represent a registered voter. '''
    
    # basic info
    last_name = models.TextField()
    first_name = models.TextField()
    dob = models.DateField()

    # address
    res_street_number = models.IntegerField()
    res_street_name = models.TextField()
    res_apartment_number = models.TextField()
    res_zip_code = models.IntegerField()

    # voting stuff
    dor = models.DateField()
    party_affiliation = models.CharField(max_length=6)
    precinct_number = models.TextField()

    # election participation
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.first_name} {self.last_name} (Precinct {self.precinct_number})"
    


def str_to_bool(s):
    return s.strip().upper() == 'TRUE'
    

def load_data():
    '''Function to load data records from CSV file into Django model instances.''' 

     # delete existing records to prevent duplicates: (DANGEROUS)
    Voter.objects.all().delete()

    filename = '/Users/winson/Desktop/School/cs412/django/datafiles/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    i = 0

    for line in f:

        i += 1
        line = line.strip()
        fields = line.split(',')
       
        try:
            # create a new instance of Result object with this record from CSV
            result = Voter( last_name=fields[1].strip(),
                            first_name=fields[2].strip(),
                            res_street_number = fields[3].strip(),
                            res_street_name = fields[4].strip(),
                            res_apartment_number = fields[5].strip(),
                            res_zip_code = fields[6].strip(),
                            dob = fields[7].strip(),
                            dor = fields[8].strip(),
                            party_affiliation = fields[9].strip(),
                            precinct_number = fields[10].strip(),
                        
                            v20state = str_to_bool(fields[11]),
                            v21town = str_to_bool(fields[12]),
                            v21primary = str_to_bool(fields[12]),
                            v22general = str_to_bool(fields[13]),
                            v23town = str_to_bool(fields[14]),
                            voter_score = fields[16].strip()
                        )
        

            result.save() # commit to database
            print(f'Created result: {result}')
            
        except:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} Results.')

