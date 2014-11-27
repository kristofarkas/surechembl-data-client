import codecs
import json
from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Sequence, Integer, String, SmallInteger, Date


def chunks(l, n):
    """ Yield successive n-sized chunks from l. Via Stack Overflow.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]



class DataLoader:

    def __init__(self, db):
        self.db = db
        self.metadata = MetaData()
        self.docs = Table('schembl_document', self.metadata,
                     Column('id',                Integer,       Sequence('schembl_document_id'), primary_key=True),
                     Column('scpn',              String(50),    unique=True),
                     Column('published',         Date()),
                     Column('life_sci_relevant', SmallInteger()),
                     Column('family_id',         Integer))

        # TODO field sizes asserted


    def db_metadata(self):
        return self.metadata


    def load(self, file_name):

        input_file = codecs.open(file_name, 'r', 'utf-8')
        biblio = json.load(input_file)

        conn = self.db.connect()

        for chunk in chunks(biblio, 5):

            transaction = conn.begin()

            # TODO Multiple inserts?
            for bib in chunk:

                # TODO empty values rejected (or accepted)

                # TODO improve handling of default list extraction
                pubdate = datetime.strptime( bib['pubdate'][0], '%Y%m%d')

                record = dict(
                    scpn              = bib['pubnumber'][0],
                    published         = pubdate,
                    family_id         = bib['family_id'][0],
                    life_sci_relevant = 1 )

                # TODO duplicate SCPN
                # TODO life science relevant function


                ins = self.docs.insert().values( record )

                result = conn.execute(ins)

                print result.inserted_primary_key

                # TODO retrieve full set of document IDs (pre-load?)
                # TODO param to disable document ID query

                # TODO titles and classifications inserted


            # TODO appropriate transaction scope
            transaction.commit()

        conn.close()
        codecs.close()









