/* $Cambridge: exim/exim-src/src/auths/cyrus_sasl.h,v 1.2 2009/11/16 19:50:38 nm4 Exp $ */

/*************************************************
*     Exim - an Internet mail transport agent    *
*************************************************/

/* Copyright (c) University of Cambridge 1995 - 2009 */
/* See the file NOTICE for conditions of use and distribution. */

/* Copyright (c) A L Digital Ltd 2004 */

/* Private structure for the private options. */

typedef struct {
  uschar *server_service;
  uschar *server_hostname;
  uschar *server_realm;
  uschar *server_mech;
} auth_cyrus_sasl_options_block;

/* Data for reading the private options. */

extern optionlist auth_cyrus_sasl_options[];
extern int auth_cyrus_sasl_options_count;

/* Block containing default values. */

extern auth_cyrus_sasl_options_block auth_cyrus_sasl_option_defaults;

/* The entry points for the mechanism */

extern void auth_cyrus_sasl_init(auth_instance *);
extern int auth_cyrus_sasl_server(auth_instance *, uschar *);
extern int auth_cyrus_sasl_client(auth_instance *, smtp_inblock *,
                                smtp_outblock *, int, uschar *, int);

/* End of cyrus_sasl.h */
