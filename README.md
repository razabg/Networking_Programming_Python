# Network Programming with Python

A comprehensive collection of network programming projects and tools built with Python, demonstrating socket programming, protocol implementation, security analysis, and cloud integration.

## 🚀 Features

### Core Networking
- **Multi-client Chat System** - TCP/UDP socket-based chat server supporting multiple concurrent clients using `select()` multiplexing
- **HTTP Server** - Custom HTTP server implementation with URL parameter parsing and request handling
- **DNS Server** - Full DNS server with A and PTR query support using Scapy, implements `nslookup` functionality

### Network Tools & Analysis
- **Network Command Suite**
  - `ping` - ICMP echo request/reply implementation
  - `traceroute` - Path discovery using TTL manipulation
  - `arp` - ARP table inspection and manipulation
  - `port scanner` - Multi-threaded port scanning utility

### Security & Research
- **SYN Flood Attack Analysis** - Traffic analysis and detection of TCP SYN flood attacks
- **TLS Research Module** - Deep dive into Transport Layer Security protocols and implementation

### Cloud Integration
- **Video Search Application** - AWS-powered video search using:
  - AWS Transcribe API for speech-to-text
  - S3 for media storage
  - NumPy and Pandas for data processing and analysis

## 🛠️ Technologies

- **Python 3.x**
- **Scapy** - Packet manipulation and network discovery
- **AWS SDK (Boto3)** - Cloud service integration
- **NumPy** - Numerical computing
- **Pandas** - Data analysis and manipulation
- **Socket Programming** - TCP/UDP protocols
- **Threading/Select** - Concurrent connection handling
```

## 🎯 Usage Examples

### Chat Server
```bash
# Start the server
python chat_system/server.py --port 5555

# Connect clients
python chat_system/client.py --host localhost --port 5555
```

### HTTP Server
```bash
# Start HTTP server
python http_server/server.py --port 8080

# Test with parameters
curl "http://localhost:8080/search?q=python&type=tutorial"
```

### DNS Server
```bash
# Start DNS server
sudo python dns_server/dns_server.py

# Perform nslookup
python dns_server/nslookup.py google.com
python dns_server/nslookup.py -type=PTR 8.8.8.8
```

### Network Tools
```bash
# Ping a host
python network_tools/ping.py google.com

# Traceroute
python network_tools/traceroute.py google.com

# Port scan
python network_tools/port_scanner.py 192.168.1.1 1-1000
```

### Video Search (AWS)
```bash
# Upload and transcribe video
python video_search/transcribe.py --video path/to/video.mp4

# Search transcriptions
python video_search/search_engine.py --query "machine learning"
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Raz Abergel**

- GitHub: [@razabergel](https://github.com/razabergel)

## 🙏 Acknowledgments

- Python Socket Programming documentation
- Scapy community and documentation
- AWS documentation and samples
- Network programming best practices from various sources

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

⭐ Star this repository if you found it helpful!
