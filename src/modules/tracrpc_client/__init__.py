#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Description: Trac XMLrpc services
# Authors: Daniel Rodriguez
# Date:
# Revision:
# Head URL:
# Last changed by: ''

import os
import time
import sys
import pprint

from urlparse import urlparse,  urlunparse
import logging
logger = logging.getLogger (__name__)

class TracXMLRPC (object):
    """Encapsulation of the XMLRPC API in Trac"""

    dform = """ Redaction: [[RedactionLink]]
-------------------------------------------------------
'''Drug names'''
{0}
-------------------------------------------------------
'''Nplids'''
{1}
-------------------------------------------------------
'''Comments'''
{2}
-------------------------------------------------------
'''Notes'''
{3}
"""
    def __init__ (self,  url,   authz_string=None):
        """Initialize Trac site located in 'url' and sign in with given authorization string in the form user:password or
        if it is not given, take it from the 'url'"""
        from xmlrpclib import ServerProxy
    ## 'http://daro:d1a2r3o4@trac.spc-01.sidi.se/login/rpc'
        if authz_string:
            parsed = list (urlparse (url) [:])
            assert parsed [1] ,  "Wrong url '%s' : %s" % (url,  parsed)
            if "@" in parsed [1]:
                parsed [1] = authz_string + "@" + parsed [1].split ("@")[1]
            else:
                parsed [1] = authz_string + "@" + parsed [1]
            url = urlunparse (parsed)
        self.trac_connection = ServerProxy (url)
        self.trac_url = url
        self.trac_domain = urlparse (url).hostname
        self._tickets_ids = []
        self._ticket_fields = {}
        self._filters = []

    def add_filter (self,  filter_function):
        self._filters.append (filter_function)

    def __iter__(self):
        return self.next ()

    def next (self):
        tickets_ids = self.tickets_ids () [:]
        for id in tickets_ids:
            ticket = TracTicket (id,  self)
            bol = all ([flt (ticket) for flt in self._filters])
            if bol:
                yield ticket
        raise StopIteration

    def ticket_query (self,  query):
        """Perform the 'query' retrieving tickets ids (integers)"""
        assert isinstance (query,  unicode)
        uquery = query.encode ("utf8")
        p = self.trac_connection
        result = p.ticket.query(uquery.replace ("&",  "\\&").replace ("|",  "\\|"))
        return map (int,  result)

    def tickets_ids (self):
        """List over all the ids in the whole ticket database"""
        if not self._tickets_ids:
            self._tickets_ids = sorted (self.ticket_query(u"max=1000000"))
        return self._tickets_ids

    def __len__(self):
        return len (self.tickets_ids())
        
    def highest_id (self):
        return self.tickets_ids () [-1]
        
    def top_ticket (self):
        return self.ticket_obj (self.highest_id)

    def has_unique_ticket (self,  summary):
        """Is there one and only one ticket with the given 'summary'?"""
        assert isinstance (summary,  unicode)
        tickets = self.ticket_query (u"summary=%s" % summary)
        return len (tickets) == 1

    def has_ticket (self,  summary):
        """Is there one ticket with the given 'summary'?"""
        assert isinstance (summary,  unicode)
        tickets = self.ticket_query(u"summary=%s" % summary)
        return len (tickets) > 0

    def tickets_ids_of_summary (self,  summary):
        """The ids (integers) of the tickets with a given 'summary'"""
        assert isinstance (summary,  unicode)
        tickets = self.ticket_query(u"summary=%s" % summary)
        return tickets

    def ticket_id (self,  summary):
        assert isinstance (summary,  unicode)
        result = None
        tickets = self.ticket_query(u"summary=%s" % summary)
        if len (tickets) == 1:
            result = tickets [0]
        elif len (tickets) > 1:
            logger.error ("More than one ticket for summary %s" % summary )
        else:
            logger.error ("Ticket %s not found" % summary )
        return result

    def ticket (self,  id):
        """Data of the ticket with given 'id', Returns [id, time_created, time_changed, attributes]"""
        assert isinstance (id,  int)
        p = self.trac_connection
        result = p.ticket.get (str(id))
        return result
        
    def ticket_obj (self,  id):
        return TracTicket (id,  self)

    def ticket_create (self,  summary,  description, fields= {}):
        """Create a ticket returning a ticket object."""
        assert isinstance (summary,  unicode)
        assert isinstance (description,  unicode)
        summary = summary.encode ('utf8')
        description = description.encode ('utf8')
        p = self.trac_connection
        id = p.ticket.create (summary,  description,  fields)
        self._tickets_ids = []
        return self.ticket_obj (id)

    def ticket_create_in_steps (self,  summary,  description, fields= {}):
        """Create a ticket and update each attibute in steps returning a ticket object."""
        assert isinstance (summary,  unicode)
        assert isinstance (description,  unicode)
        summary = summary.encode ('utf8')
        description = description.encode ('utf8')
        p = self.trac_connection
        id = p.ticket.create (summary,  description,  {})
        if id:
            t = self.ticket_obj (id,  self)
            for fld in fields:
                t.set_attribute (fld, fields [fld])
        self._tickets_ids = []
        return t

    def ticket_remove (self,  id):
        assert isinstance (id,  int)
        p = self.trac_connection
        result = p.ticket.delete (str(id))
        self._tickets_ids = []
        return result

    def tickets_fields (self):
        if not self._ticket_fields:
            p = self.trac_connection
            result = p.ticket.getTicketFields ()
            self._ticket_fields = {r ['name']: r for r in result }
        return self._ticket_fields

    def ticket_changelog (self,  id):
        assert isinstance (id,  int)
        p = self.trac_connection
        result = p.ticket.getChangelog (str(id))
        return result


class TracTicket (object):
    def __init__ (self,  id,  trac):
        self.trac = trac
        self.id = id
        self._created = None
        self._changed = None
        self._attributes = {}
        self.load_data ()

    def load_data (self):
        id,  self._created,  self._changed,  self._attributes = self.trac.ticket (self.id)
        assert id == self.id
        self._fields = self.trac.tickets_fields ()

    def attributes (self):
        """Data of the ticket. This data can be used when importing into another trac of same type"""
        assert self._attributes,  "invalid ticket %i" % self.id
        result = self._attributes.copy ()
        del result ['time']
        del result ['changetime']
        return result

    def summary (self):
        """Summary of the ticket"""
        return self.field_value (u'summary')

    def time (self):
        assert self._attributes,  "invalid ticket %i" % self.id
        result = self._attributes [3]['time']
        return result

    def changetime (self):
        assert self._attributes,  "invalid ticket %i" % self.id
        result = self._attributes [3]['changetime']
        return result

    def attributes_values (self,  fields=[]):
        """a dictionary with (field,values) for each field which is a valid field for the ticket"""
        assert self._attributes,  "invalid ticket %i" % self.id
        values = {f: self.ticket_out ().get (f,  u'') for f in fields if f in self._fields}
        return values

    def attribute_value (self,  fld):
        assert self._attributes,  "invalid ticket %i" % self.id
        result = self.attributes_values (fields=[fld]).get (fld, u'')
        if isinstance (result,  str):
            result = unicode (result,  'utf8')
        return result

    def set_attribute (self,  fld,  value=u'',  set_action=[],  comm=u''):
        assert self._attributes,  "invalid ticket %i" % self.id
        assert  fld in self._fields
        if isinstance (value,  bool): value = int (value)
        if isinstance (value, int): value= unicode (value)
        assert isinstance (value,  unicode)
        data = self.attributes ()
        #data ['action'] = set_action
        data [fld] = value
        u = self.trac.trac_connection.ticket.update (self.id,"XMLRPC: %s attribute %s -->> %s. %s" % (self.id,  fld,  data [fld],  comm), data)
        assert self.id == u [0]
        self._created = u [1]
        self._changed = u [2]
        self._attributes = u [3].copy()
        logger.info ("Ticket : %s attribute %s -->> %s. %s" % (self.id,  fld,  data [fld],  comm))

    def rename_ticket (self, new_summary,  set_action='leave',  comm=u''):
        assert isinstance (new_summary,  unicode)
        self.set_field (u'summary',  value=new_summary,  set_action=set_action,  comm=comm)

    def log (self):
        """Changes historically logged"""
        assert self._attributes,  "invalid ticket %i" % self.id
        result = self.trac.ticket_changelog (self.id)
        return result

    def last_change (self,  ticket_id):
        """Date for last approval of the ticket 'ticket_id', None if not has been any approval yet"""
        assert self._attributes,  "invalid ticket %i" % self.id
        result = self.log() [-1]
        return result

    def remove (self):
        """Remove the ticket."""
        assert self._attributes,  "invalid ticket %i" % self.id
        result = self.trac.ticket_remove (self.id)
        return result

    def actions (self):
        assert self._attributes,  "invalid ticket %i" % self.id
        actions = self.trac.trac_connection.ticket.getActions(self.id)
        return actions

    def generated_ticket_description (self, rec, dform):
        for k in rec:
            if isinstance (rec [k],  unicode):
                rec [k] = rec [k].encode ("utf8")
        result = self.dform.format ('\n' .join (rec ['lname']),
                     '\n' .join (["[" + rec ['lv_uris'][i] + " " + v + "]" for i, v in enumerate (rec ['nplids'])]),
                     '\n' .join (rec ['comments']),
                     '\n' .join (rec ['notes']))
        return result

def test0 (args):
    url = args.trac_url
    db = TracXMLRPC (url)
    if len (db) > 10:
        logger.error ("The ticket database has to be empty!")
        sys.exit (-1)
    ticket = db.ticket_create (u"What?",  u" What? .. i h .. te")
    logger.info ("--- Ticket %i" % ticket.id)
    logger.info (pprint.pformat (ticket._attributes))
    time.sleep (20)
    a = ticket.actions ()
    logger.info (pprint.pformat(a))
    ticket.set_attribute ("atc", u"A01")
    a = ticket.actions ()
    logger.info (pprint.pformat(a))
    logger.info ("Deleting all the tickets")
    for t in db:
        logger.info ("Deleting ticket id:%i" % t.id)
        i = t.remove ()
        logger.info ("Removed, returned: %i",  i)
    logger.info ("Available fields in database")
    logger.info (pprint.pformat (db.tickets_fields()))


def main ():
    import argparse
    parser = argparse.ArgumentParser(description="Synchronize publishing and news.")
    parser.add_argument('-u','--trac-url', help='Url to Trac,  e.g.:http://daro:d1a2r3o4@trac.spc-01.sidi.se/login/rpc')
    parser.add_argument('-v','--verbose', action="store_true",  default=False)
    parser.add_argument('-q','--quiet', action="store_true",  default=False)
    #parser.add_argument('-f','--file', help='A specific file containing a list of tickets')
    parser.add_argument('-i','--id', help='Document id')
    ## actions
    parser.add_argument('command', help="""Perform command. Valid values: test0""")
    args = parser.parse_args()


    global verbose_output

    if args.quiet:
        handler = logging.NullHandler()
    else:
        handler = logging.StreamHandler(sys.stdout)

    verbose_output = args.verbose
    if verbose_output:
        handler.setFormatter (logging.Formatter ("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler (handler)
        logger.setLevel (logging.DEBUG)
    else:
        handler.setFormatter (logging.Formatter ("%(levelname)s - %(name)s - %(message)s"))
        logger.addHandler (handler)
        logger.setLevel (logging.INFO)

    if args.command == 'test0':
        test0 (args)
    else:
        logging.error("""Unknown or unexistent command:%s. Has to be one of test0: """ % args.command)

if __name__ == '__main__':
    main ()
