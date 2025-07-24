from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
import os
def split_string(s, chunk_size=5000):
    return [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]
def generate_self_signed_cert(
    subject_dict,
    valid_days=365,
    key_size=2048,
    output_cert="certificate.crt",
    output_key="private.key"
):
    """
    生成自签名证书
    
    参数:
    subject_dict - 包含主题信息的字典，键包括：
        "C"   - 国家 (Country)
        "ST"  - 州/省 (State/Province)
        "L"   - 城市 (Locality)
        "O"   - 组织 (Organization)
        "OU"  - 组织单位 (Organizational Unit)
        "CN"  - 通用名称 (Common Name)
    valid_days - 证书有效期天数 (默认365天)
    key_size - RSA密钥长度 (默认2048位)
    output_cert - 证书输出文件名
    output_key - 私钥输出文件名
    """
    issuer_subject_dict = {
        "C": 'cc',              # 国家
        "ST": 'st',        # 省
        "L": 'l',         # 城市
        "O": "o",    # 组织
        "OU": 'ou',    # 组织单位
        "CN": "cn",    # 通用名称
    }
    # 生成RSA私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    
    # 准备主题信息
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, subject_dict["C"]),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, subject_dict["ST"]),
        x509.NameAttribute(NameOID.LOCALITY_NAME, subject_dict["L"]),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject_dict["O"]),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, subject_dict["OU"]),
        x509.NameAttribute(NameOID.COMMON_NAME, subject_dict["CN"]),
    ])
    issuer_subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, issuer_subject_dict["C"]),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, issuer_subject_dict["ST"]),
        x509.NameAttribute(NameOID.LOCALITY_NAME, issuer_subject_dict["L"]),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, issuer_subject_dict["O"]),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, issuer_subject_dict["OU"]),
        x509.NameAttribute(NameOID.COMMON_NAME, issuer_subject_dict["CN"]),
    ])
    
    # 设置有效期
    valid_from = datetime.utcnow()
    valid_to = valid_from + timedelta(days=valid_days)
    
    # 构建证书
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer_subject)  ###改了# 自签名证书，颁发者=主题
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_to)
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None), 
            critical=True
        )
    )
    
    # 签名证书
    certificate = builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA256(),
    )
    
    # 保存私钥
    with open(output_key, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    
    # 保存证书
    with open(output_cert, "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))
    
    return certificate, private_key

def modcert(save_name,c='WW',st='ST',l='L',o='O',ou='OU',cn='CN',valid_days=730):# 生成证书（有效期为2年）
    # 自定义主题信息
    #手机只显示CN,O,OU。CN最大64
    subject_info = {
        "C": c,              # 国家
        "ST": st,        # 省
        "L": l,         # 城市
        "O": o,    # 组织
        "OU": ou,    # 组织单位
        "CN": cn,    # 通用名称
    }
    
    
    cert, key = generate_self_signed_cert(
        subject_dict=subject_info,
        valid_days=valid_days,
        output_cert=save_name+".crt",
        output_key=save_name+".key"
    )
    
    print(f"证书已生成: my_certificate.crt")
    print(f"私钥已生成: my_private_key.key")
    #print(f"\n证书主题: {cert.subject}")
    print(f"有效期: {cert.not_valid_after - cert.not_valid_before} days")
    print(f"序列号: {cert.serial_number}")
title=input('标题：')+'-'
input_text=open(input('路径:'),encoding='UTF-8',mode='r').read()
input_text=split_string(input_text,chunk_size=10000)
for i in range(0,len(input_text)):#单次10000
	now_text=title+str(i).zfill(3)+'\n--------------------\n'+input_text[i]
	modcert('output/'+title+str(i).zfill(3),o=title+str(i).zfill(3),cn=input_text[i][:15]+'......',ou=now_text)
