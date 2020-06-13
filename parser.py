movies              = []
directors           = []
actors              = []
actresses           = []
names_and_durations = []
names               = []

OWL_FILENAME  = 'cinema_database.owl'
OWL_FULL_ONTO = 'cinema_full.owl'

# Movie keys
MOVIE_LABEL = 0
MOVIE_YEAR  = 1

# Director keys
DIRECTOR_MOVIE = 0
DIRECTOR_LABEL = 1

# Actor keys
ACTOR_MOVIE     = 0
ACTOR_LABEL     = 1
ACTOR_CHARACTER = 2

# Actress keys
ACTRESS_MOVIE     = 0
ACTRESS_LABEL     = 1
ACTRESS_CHARACTER = 2

# Movie keys
ND_MOVIE    = 0
ND_NAME     = 1
ND_DURATION = 2

# Person keys
NAME_LABEL  = 0
NAME_FIRST  = 1
NAME_FAMILY = 2

def writeFullOntologyOwl():
    with open('cinema.owl', 'r') as fp:
        onto_file_str = fp.read()
        idx = onto_file_str.rfind(')')

        with open('cinema_database.owl', 'r')  as fp_db:
            database_str = fp_db.read()

            full_onto = onto_file_str[:idx] + database_str + ')\n'

            try:
                full_fp = open(OWL_FULL_ONTO, 'w')
                full_fp.write(full_onto)
            finally:
                full_fp.close()

# Write an OWL file with the parsed data
def writeOwl():
    try:
        fp = open(OWL_FILENAME, 'w')
        
        # Declaration(NamedIndividual(:Individual))
        for individual in movies:
            fp.write('Declaration(NamedIndividual(:' + individual[MOVIE_LABEL] + '))\n')

        for individual in directors:
            fp.write('Declaration(NamedIndividual(:' + individual[DIRECTOR_LABEL] + '))\n')

        for individual in actors:
            fp.write('Declaration(NamedIndividual(:' + individual[ACTOR_LABEL] + '))\n')

        for individual in actresses:
            fp.write('Declaration(NamedIndividual(:' + individual[ACTRESS_LABEL] + '))\n')

        fp.write('\n\n############################\n')
        fp.write('#   Named Individuals\n')
        fp.write('############################\n\n')

        # ClassAssertion(:Movie :movie_label)
        for individual in movies:
            fp.write('ClassAssertion(:Movie :' + individual[MOVIE_LABEL] + ')\n')
        fp.write('\n')

        # ClassAssertion(:Director :director_label)
        for individual in directors:
            fp.write('ClassAssertion(:Director :' + individual[DIRECTOR_LABEL] + ')\n')
        fp.write('\n')
        
        # ClassAssertion(:Actor :actor_label)
        for individual in actors:
            fp.write('ClassAssertion(:Actor :' + individual[ACTOR_LABEL] + ')\n')
        fp.write('\n')
        
        # ClassAssertion(:Actress :actress_label)
        for individual in actresses:
            fp.write('ClassAssertion(:Actress :' + individual[ACTRESS_LABEL] + ')\n')
        fp.write('\n\n')

        # DataPropertyAssertion(:year :movie_label "year"^^xsd:unsignedLong)
        for individual in movies:
            fp.write('DataPropertyAssertion(:year :' + individual[MOVIE_LABEL] + ' "' + individual[MOVIE_YEAR] + '"^^xsd:unsignedLong)\n')
        fp.write('\n\n')

        # DataPropertyAssertion(foaf:firstName :label "FirstName")
        # DataPropertyAssertion(foaf:familyName :label "FamilyName")
        for individual in names:
            fp.write('DataPropertyAssertion(foaf:firstName :' + individual[NAME_LABEL] + ' "' + individual[NAME_FIRST] + '")\n')
            fp.write('DataPropertyAssertion(foaf:familyName :' + individual[NAME_LABEL] + ' "' + individual[NAME_FAMILY] + '")\n')
        fp.write('\n\n')

        # DataPropertyAssertion(foaf:name :label_movie "Movie Name")
        # DataPropertyAssertion(:duration :label_movie "Duration"^^xsd:unsignedLong)
        for individual in names_and_durations:
            fp.write('DataPropertyAssertion(foaf:name :' + individual[ND_MOVIE] + ' "' + individual[ND_NAME] + '")\n')
            fp.write('DataPropertyAssertion(:duration :' + individual[ND_MOVIE] + ' "' + individual[ND_DURATION] + '"^^xsd:unsignedLong)\n')
        fp.write('\n\n')

        # ObjectPropertyAssertion(:directs :director_label :movie_label)
        for individual in directors:
            fp.write('ObjectPropertyAssertion(:directs :' + individual[DIRECTOR_LABEL] + ' :' + individual[DIRECTOR_MOVIE] + ')\n')
        fp.write('\n\n')

        # Declaration(NamedIndividual(:Individual))
        # Declaration(NamedIndividual(:Individual))
        # ClassAssertion(:Character :character_label)
        # ClassAssertion(:Role :role_label)
        # ObjectPropertyAssertion(:interprets :actor_label :character_label)
        # ObjectPropertyAssertion(:performsOn :actor_label :movie_label)
        # ObjectPropertyAssertion(:hasActor :role_label :actor_label)
        # ObjectPropertyAssertion(:hasCharacter :role_label :character_label)
        # ObjectPropertyAssertion(:hasRole :movie_label :role_label)
        unamed_count = 1
        for individual in actors:
            character_label = None
            if individual[ACTOR_CHARACTER] == '':
                character_label = 'unamed_character' + str(unamed_count)
                unamed_count += 1
            else:
                character_label = 'character_' + individual[ACTOR_CHARACTER]

            fp.write('Declaration(NamedIndividual(:' + character_label + '))\n')
            
            role_label = individual[ACTOR_MOVIE] + '_' + character_label
            fp.write('Declaration(NamedIndividual(:' + role_label + '))\n')
            
            fp.write('ClassAssertion(:Character :' + character_label + ')\n')
            fp.write('ClassAssertion(:Role :' + role_label + ')\n')

            fp.write('ObjectPropertyAssertion(:interprets :'   + individual[ACTOR_LABEL] + ' :' + character_label + ')\n')
            fp.write('ObjectPropertyAssertion(:performsOn :'   + individual[ACTOR_LABEL] + ' :' + individual[ACTOR_MOVIE] + ')\n')
            fp.write('ObjectPropertyAssertion(:hasActor :'     + role_label + ' :' + individual[ACTOR_LABEL] + ')\n')
            fp.write('ObjectPropertyAssertion(:hasCharacter :' + role_label + ' :' + character_label + ')\n')
            fp.write('ObjectPropertyAssertion(:hasRole :'      + individual[ACTOR_MOVIE] + ' :' + role_label + ')\n')
        fp.write('\n\n')

        # Declaration(NamedIndividual(:Individual))
        # Declaration(NamedIndividual(:Individual))
        # ClassAssertion(:Character :character_label)
        # ClassAssertion(:Role :role_label)
        # ObjectPropertyAssertion(:interprets :actress_label :character_label)
        # ObjectPropertyAssertion(:performsOn :actress_label :movie_label)
        # ObjectPropertyAssertion(:hasActress :role_label :actress_label)
        # ObjectPropertyAssertion(:hasCharacter :role_label :character_label)
        # ObjectPropertyAssertion(:hasRole :movie_label :role_label)
        for individual in actresses:
            character_label = None
            if individual[ACTRESS_CHARACTER] == '':
                character_label = 'unamed_character' + str(unamed_count)
                unamed_count += 1
            else:
                character_label = 'character_' + individual[ACTRESS_CHARACTER]

            fp.write('Declaration(NamedIndividual(:' + character_label + '))\n')
            
            role_label = individual[ACTRESS_MOVIE] + '_' + character_label
            fp.write('Declaration(NamedIndividual(:' + role_label + '))\n')
            
            fp.write('ClassAssertion(:Character :' + character_label + ')\n')
            fp.write('ClassAssertion(:Role :' + role_label + ')\n')

            fp.write('ObjectPropertyAssertion(:interprets :'   + individual[ACTRESS_LABEL] + ' :' + character_label + ')\n')
            fp.write('ObjectPropertyAssertion(:performsOn :'   + individual[ACTRESS_LABEL] + ' :' + individual[ACTRESS_MOVIE] + ')\n')
            fp.write('ObjectPropertyAssertion(:hasActress :'   + role_label + ' :' + individual[ACTRESS_LABEL] + ')\n')
            fp.write('ObjectPropertyAssertion(:hasCharacter :' + role_label + ' :' + character_label + ')\n')
            fp.write('ObjectPropertyAssertion(:hasRole :'      + individual[ACTRESS_MOVIE] + ' :' + role_label + ')\n\n')
        fp.write('\n')

    finally:
        fp.close()

def getParameters(line):
    idx = 0;
    
    # find '('
    while line[idx] != '(':
        idx += 1
    idx += 1

    # check invalid characters: [" ", "'"]
    while line[idx] == ' ' or line[idx] == "'":
        idx += 1

    # parsing
    param_str = ''
    parameters = []
    while line[idx] != ')':
        while line[idx] == ' ':
            idx += 1

        # string parser
        if line[idx] == "'":
            idx += 1
            while line[idx] !=  "'":
                # validating ' on words: "je t'aime"
                if line[idx] == '\\' and line[idx+1] == "'":
                    idx += 1

                param_str += line[idx]
                idx += 1 
            
            # next parameter or end of parameters
            while line[idx] != ',' and line[idx] != ')':
                idx+=1
        # other parameters
        else:
            while line[idx] != ',' and line[idx] != ')':
                param_str += line[idx]
                idx += 1

        parameters.append(param_str)
        param_str = ''

        if line[idx] != ')':
            idx += 1

    return parameters

# parse each line of .pl file
def parseLine(line):
    if line[0].isalpha():
        params = getParameters(line)
        if line.find('filme') == 0:
            movies.append(params)
        elif line.find('diretor') == 0:
            directors.append(params)
        elif line.find('ator') == 0:
            actors.append(params)
        elif line.find('atriz') == 0:
            actresses.append(params)
        elif line.find('tit_dur') == 0:
            names_and_durations.append(params)
        elif line.find('nome') == 0:
            names.append(params)

# read all lines from the prolog file simple_cinema_database.pl and writes an OWL file on the
# required format
def main():
    with open('simple_cinema_database.pl', 'r') as fp:
        print('Parsing simple_cinema_database.pl file...')
        # Read line-by-line
        line = fp.readline()
        cnt = 1

        while line:
            parseLine(line)
            line = fp.readline()
            cnt += 1

        fp.close()

    print('Writing OWL file...\n')
    writeOwl()

    print('File successfully parsed.')
    print(OWL_FILENAME + ' created.\n')

    print('Creating the complete ontology file...')
    writeFullOntologyOwl()
    print(OWL_FULL_ONTO + ' created successfully.\n')

if __name__ == "__main__":
    main()