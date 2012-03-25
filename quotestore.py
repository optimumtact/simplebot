from linebuffer import Line

#dictionary of names storing the id's of each name
name_dictionary = dict()

#list of quotes, location in the list is the quotes id number
quote_list = []

#list of unused_id's, this corresponds to spaces left in the quote_list from deletions, adding
#quotes should prefer to fill these first
unused_id_list = []

#defines the maximum number of quotes to store, default is -1 which is no limit
max_quotes = 0

def initalise(filename, maximum_quotes_to_store=-1):
  #local variables
  global name
  global max_quotes
  max_quotes = maximum_quotes_to_store
  #TODO make this support when there is no file to be opened
  f = open(filename, 'r')
  lines = f.readlines()
  
  #loop through the file and read and parse each line adding it to the appropriate lists
  count = 0
  while f.readable():
    line = parse_line(f)
    if line:
      add_name_mapping(line[name])
      add_quote(line, False)
     
    else:
      add_unused_id(count)

    count+=1

#if the given name exists in the dictionary then add that name->list_id mapping, if it doesn't then
#add the name to the dictionary and set up its id list with the given list_id
def add_name_mapping(name, list_id):
  global name_dictionary
  if name in name_dictionary:
    name_dictionary[name].append(list_id)
  else:
    name_dictionary[name]=[list_id]

  return true

#remove a given name->list_id mapping
def remove_name_mapping(name, list_id):
  global name_dictionary
  name_dictionary[name].remove(quote_id)

#add the unused_id to the global unused_id's list
def add_unused_id(unused_id):
  global unused_id_list
  unused_id_list.append(unused_id)
  return True

#get an unused_id, method returns None if no id's are spare
def get_unused_id():
  global unused_id_list
  if len(unused_id_list) > 0:
    return unused_id_list.pop(1)
  else:
    return None

#add a quote to the global quote_list, if use_unused_id is false then it will not attempt to fill
#empty spaces in the quote_list, will return -1 if the maximum number of quotes to store is hit
def add_quote(quote, name, time,  use_unused_id=True):
  global quote_list
  global max_quotes
  
  if max_quotes <= len(quotelist):
    return ['The maximum number of quotes has been exceeded, your quote has not been added']
  spare_id = None
  temp = Line()
  temp.quote =quote
  temp.name = name
  temp.time = time
  if use_unused_id:
    #attempt to grab an unused ID from the list
    spare_id = get_unused_id()

  if spare_id:
    #fill the unused space and return it's id
    quote_list[spare_id] = temp
    add_name_mapping(name, spare_id)
    quote_id = spare_id

  else:
    #append quote to end of quote list and return it's id
    quote_list.append(quote)
    add_name_mapping(quote[name], len(quote_list) - 1)
    quote_id = len(quote_list)-1

  return ['Quote:' + quote + ' from ' + name + 'has ID ' + quote_id]

#set the quote linked to quote_id to none and return the old quote to the caller
def remove_quote(quote_id):
  global quote_list

  if len(quote_list)-1 > quote_id and quote_list[quote_id]:
  
    old_quote=quote_list[quote_id]
    quote_list[quote_id] = None
    remove_name_mapping(old_quote.name, quote_id)
    add_unused_id(quote_id)
    return [format_quote_for_display(old_quote) + 'removed']
  
  else:
    return['I have no quote at ' + quote_id + ' to remove']

#find and return the quote whose id is quote_id
def get_quote(quote_id):
  global quote_list
  if len(quote_list)-1 > quote_id and quote_list[quote_id]:
    quote = quote_list[quote_id] 
    return [format_quote_for_display(quote)]

  else:
    return ["I have no quote with that id"]

#return a list of all quotes associated with the name name
def get_quotes_by_name(name):
  global name_dictionary
  global quote_list
  if name in name_dictionary:
    local_quotes = []
    quote_ids = name_dictionary[name]
    if len(quote_ids) > 0:
      for quote_id in quote_ids:
       local_quotes.append(quote_list[quote_id])
    return local_quotes
    
    else:
      return [" I have no quotes for that user"]

  else:
    return ["I have no quotes for that user"]

#find and return a list of quotes in the given range
def get_quote_range(start_id, end_id):
  global quote_list
  #if we have a bad range input we warn them!
  if end_id - start_id < 0:
    return ["Please enter an end_id larger than the start_id"]

  result=[]
  for quote_id in range(start_id, end_id):
    try:
      #if the quote is not None
      if quote_list[quote_id]:
        result.append(quote_list[quote_id])
    
    #if we run out of items in the list then we are done
    except IndexError:
      break
  
  if len(results) > 0:
    list_of_quotes=[]
    for quote in result:
      quote=format_quote_for_display(quote)
      list_of_quotes.append(quote)

    return list_of_quotes

  else:
    return ['I have no quotes for that range']
    
#write all saved quotes out to file
def flush(filename):
  global quote_list
  for line in quote_list:
    result += format_quote_for_storage(line)
  store_quotes_in_file(result, filename)

#given a file, return a single quote in the form (time, name, quote) or a None for a blank space
def parse_line(f):
  head = f.readline()
  if head is '[Quote]':
    time = f.readline()
    name = f.readline()
    quote = f.readline()
    return (time, name, quote)
  else:
    return None

#store a list of quotes the file given by filename
def store_quotes_in_file(quotes, filename):
  f = open(filename, 'w')
  f.writelines(quotes)
  return true

#return a quote split into a list of lines for storing into a flat file
def format_quote_for_storage(quote):
  result = None
  if quote:
    result = ['[Quote]\n']
    result.append(quote.name + '\n')
    result.append(quote.time + '\n')
    result.append(quote.quote + '\n')
    return result
  else:
    result = ['[Null Quote]\n']
    return result

#format a given quote into a string suitable for display
def format_quote_for_display(quote):
  return '[' + quote.time + '] <' + quote.name + '> :' + quote.quote
