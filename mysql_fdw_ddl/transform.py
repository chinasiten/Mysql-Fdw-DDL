from sqlalchemy import schema
from sqlalchemy import create_engine,Table,MetaData
from sqlalchemy.ext.compiler import compiles
import decimal
import datetime

trans_dict ={bool:'bool',
             float:'real',
             int:'integer',
             str:'varchar',
             decimal.Decimal:'numeric',
             datetime.date:'date',
             datetime.datetime:'timestamp',
             datetime.time:'time',
             datetime.timedelta:'interval'
            }

@compiles(schema.CreateColumn)
def compile(element, compiler, **kw):
    column = element.element

    text = "%s %s" % (
            column.name,
            trans_dict.get(column.type.python_type,'text')
        )
    
    return text

class MysqlFdwDDL:

      def __init__(self,url,
                        table_name,
                        server_name,
                        dbname,
                        ftschema=None):
          self.url=url
          self.table_name = table_name
          self.server_name = server_name
          self.dbname = dbname
          self.ftschema = ftschema
          self.connect()
          self.get_table_instance()

      def connect(self):
          self.engine = create_engine(self.url)

      def get_table_instance(self):
          metadata = MetaData() 
          self.table = Table(self.table_name, 
                             metadata, 
                             autoload=True, 
                             autoload_with=self.engine)

      def get_create_statment(self):
          preview = schema.CreateTable(self.table).__str__()
          ftschema = self.dbname if self.ftschema is None else self.ftschema
          preview = preview.replace(self.table_name,ftschema+'.'+self.table_name)
          drop_primary = ','.join([i for i  in preview.split(',') if 'PRIMARY KEY' not in i])
          server = drop_primary + ") server {} OPTIONS (dbname '{}', table_name '{}');".format(self.server_name,
                                                                                               self.dbname,
                                                                                               self.table_name)
          final_sql=server.replace('TABLE','FOREIGN TABLE')
          return final_sql