# -*- coding:utf-8 -*-

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import glob
import sys
import zipfile

# argv[1] = subject
# argv[2] = folder
# argv[3] = to_addr

smtp = smtplib.SMTP( 'mail.techwing.co.kr', 587 )
smtp.starttls()
smtp.login( 'wonyong.lee@techwing.co.kr', 'wonyong.lee1' )

msg = MIMEMultipart('alternative')


def set_attach_file( _file_path ) :
	mime_base = MIMEBase( 'application', 'octet-stream' )
	file = open( _file_path, 'rb' )
	mime_base.set_payload( file.read() )
	mime_base.add_header( 'Content-Disposition', 'attachment; filename="%s"'% os.path.basename( _file_path ) )
	encoders.encode_base64( mime_base )
	return mime_base

def set_content( _file_path ) :
	html = 'Cpp Check Report 입니다. 세부사항은 압축파일을 확인해 주세요.'
	html += open( _file_path, 'rt' ).read()
	contents = MIMEText( html, 'html' )
	return contents

			
def zip_folder( _folder_path ) :
	zip_file_name = _folder_path + '\\CppCheckReport.zip'
	zip = zipfile.ZipFile( zip_file_name, 'w' )
	file_list = glob.glob( _folder_path + '*.*' )
	for file_path in file_list :
		if file_path.endswith( '.zip' ) == False :
			zip.write(os.path.join(_folder_path, file_path), file_path, compress_type = zipfile.ZIP_DEFLATED)

	zip.close()
	return zip_file_name

def main() :
	msg[ 'Subject' ] = sys.argv[1]
	folder_path = sys.argv[2] # 'C:\\CppCheckReport_SLT_MP\\SLT_MC\\' # 

	argv_cnt = len( sys.argv )
	to_addr_list = []
	for i in range( 3, argv_cnt ) :
		to_addr_list.append( sys.argv[i] )

	msg[ 'To' ] = ", ".join( to_addr_list ) 
	msg_to = to_addr_list 
	
	
	file_list = glob.glob( folder_path + '*.*' )
	for file_path in file_list :
		if file_path.find( 'index' ) > 0 :
			msg.attach( set_content( file_path ) )
		elif file_path.find( 'style' ) > 0 :
			msg.attach( set_attach_file( file_path ) )
	
	
	zip_file_name = zip_folder( folder_path )
	msg.attach( set_attach_file( zip_file_name ) )


	smtp.sendmail( 'wonyong.lee@techwing.co.kr', msg_to, msg.as_string() )
	smtp.quit()


	
main()








