import click
from .crypto import encrypt_file, decrypt_file

@click.group()
def cli():
    """EncryptX Pro CLI"""
    pass

@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def encrypt(input_path, output_path):
    """Encrypt a file"""
    encrypt_file(input_path, output_path)
    click.echo("✅ Encryption complete.")

@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def decrypt(input_path, output_path):
    """Decrypt a file"""
    decrypt_file(input_path, output_path)
    click.echo("✅ Decryption complete.")

if __name__ == '__main__':
    cli()
