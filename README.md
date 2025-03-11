# DNS Optimizer

## Project Description

**DNS Optimizer** is a Python script that helps optimize your DNS settings by testing multiple public DNS servers (such as Google DNS, Cloudflare, OpenDNS, etc.) and selecting the fastest one based on response times. The script works on both **Windows** (via WSL) and **Linux** systems, providing an easy-to-use solution to enhance network performance by applying the best DNS server to your system.

## Features

- Tests and compares the response times of popular DNS servers like Google, Cloudflare, OpenDNS, and more.
- Selects the fastest DNS server based on ping results.
- Optionally applies the best-performing DNS server to your system’s network settings.
- Cross-platform support for **Windows** and **Linux**.
- Simple and user-friendly interface.

## Requirements

- Python 3.x
- Libraries: `requests`, `pandas`, `icmplib`, `fireducks`

## Installation

### 1. Clone this repository

```bash
git clone https://github.com/your-username/dns-optimizer.git
cd dns-optimizer
