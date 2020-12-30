zDLP - a corporate DLP (Data Loss/leakage Prevention) system
-------------------------------------------------------------
written in Python
'''
Data loss prevention software detects potential data breaches/data ex-filtration transmissions
and prevents them by monitoring, detecting and blocking sensitive data while in use (endpoint actions),
in motion (network traffic), and at rest (data storage).
'''
Today features:
Client-server architecture: (Where Server - agent on checked host and Client is host-manager) ;
CLI manage;
Scan & Check files (of many types, including images) on agent host for text patterns;
Scan & Check files on agent host in archives (.rar), applying a list of predefined passwords;
Save results to SQLite DB;


2020.12.11 - Initial Pre Alpha version

Roadmap:
Initial functionality 
	Client-server (XML-RPC)
	Scan directory tree
	Store paths and other info in DB
	Extract text from paths
	Search for RE in extracted text
Work with containers (easy way: like with single file, don't store contained paths in DB)
	rar
	zip
