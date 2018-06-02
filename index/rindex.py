from optparse import OptionParser

# Usage:
# rindex.py -T job/flow_name.txt -D job/flow_days.txt
# log: /log/index

SOLR_URL = ''
POST_JAR_URL = 'opt/cloudera/parcels/CDH/jars/post.jar'

single_day = ''
solr_server=''
collection = ''
json_loc_base = '/usr/indexer/'
json_loc = ''
index_command_base = 'java -Dtype=application/json -Drecursive -Durl='
index_command = ''
solr_instance_detail = ''

class rindex():
    def __init__(self, solr_server=None, collection=None, flow_name=None, flow_days=None):
        self.json_file = ''
        self.process_options(solr_server, collection, flow_name, flow_days)

    def process_options(self, solr_server, collection, flow_name, flow_days):
        parser = OptionParser()
        parser.add_option("-s", "--solr_instance_detail", dest="solr_instance_detail", help="Enter solr_instance_detail")
        #parser.add_option("-c", "--collection", dest="collection", help="Enter solr collection")
        parser.add_option("-f", "--flow_name", dest="flow_name", help="Enter flow_name file")
        parser.add_option("-d", "--flow_days", dest="flow_days", help="enter flow_day file")

        (options, args) = parser.parse_args()

        if not options.solr_instance_detail:
            if not solr_server:
                parser.error('solr_server not provided (-s solr_server)')
        else:
            with open(options.solr_instance_detail) as f:
                the_solr_instance_detail = f.readlines()
            solr_server = the_solr_instance_detail[0].split('|')[0]
            collection = the_solr_instance_detail[0].split('|')[1]


        if not options.flow_name:
            if not flow_name:
                parser.error('flow name not provided (-f option)')

        if not options.flow_days:
            if not flow_days:
                parser.error('flow days not provided (-d option)')

        #self.options = options
        self.read_flow_days(options.flow_days, options.flow_days)

    def read_file(self, filename):
        try:
            f = open(filename, 'r')
        except:
            self.logger.error('Error while reading ' + filename)

    def single_rindex(self, json_loc):

        # print warning?
        # read solr server and compose the SOLR_URL
        SOLR_URL = 'http://' + solr_server + '.nam.nsroot.net:8983/solr/' + collection + '/update/json/docs'
        # reaad entries from flow_days
        index_command = index_command_base + SOLR_URL + ' -jar ' + POST_JAR_URL + ' ' + single_day + ' ' + json_loc

        print(index_command)
        # os.system(single_command)

    def read_flow_days(self, flow_name, flow_days):
        with open(flow_days) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]

        # now we have the date for the json files to be indexed
        for i, each_date in enumerate(content):
            json_loc = json_loc_base + flow_name + '/json/' + each_date
            #print(json_loc)
            self.single_rindex(json_loc)
        return i + 1

    def run(self):
        print('\nDone!')

if __name__ == '__main__':
    rindex().run()