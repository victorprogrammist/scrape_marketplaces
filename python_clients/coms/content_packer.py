
import io
import zipfile
import gzip
import zlib
import json


BOM_UTF8 = b'\xef\xbb\xbf'

def is_json(data: bytes):

    data = data.strip()
    if not data:
        return False

    if data.startswith(BOM_UTF8):
        data = data[len(BOM_UTF8):]

    return data.startswith(b'{') and data.endswith(b'}')


def is_zlib(data: bytes) -> bool:

    if len(data) < 2:
        return False

    # 1. Проверяем, что метод сжатия равен 8 (DEFLATE)
    # и размер окна не превышает корректные 32КБ (старшие 4 бита <= 7)
    if (data[0] & 0x0F) != 8 or (data[0] >> 4) > 7:
        return False

    # 2. Проверяем контрольный бит заголовка по правилу деления на 31
    header_checksum = (data[0] << 8) + data[1]
    return header_checksum % 31 == 0


def pack_to_zipfile(data: bytes, filename: str = "answer.dat") -> bytes:

    # 1. Создаем байтовый буфер в памяти
    zip_buffer = io.BytesIO()

    # 2. Открываем ZipFile для записи в этот буфер
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        # 3. Записываем бинарные данные внутрь архива с указанным именем файла
        z.writestr(filename, data)

    # 4. Возвращаем сырые байты готового ZIP-архива
    return zip_buffer.getvalue()


def __try_decompress(data: bytes):

    # 1. Сначала строго ZIP (у него самая жесткая структура и метаданные)
    if data.startswith(b'PK\x03\x04'): # Быстрая проверка сигнатуры ZIP
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                return 'zipfile', z.read(z.namelist()[0])
        except:
            pass

    # 2. Затем GZIP (контролирует магические байты \x1f\x8b и CRC32 в конце)
    if data.startswith(b'\x1f\x8b'): # Быстрая проверка сигнатуры GZIP
        try:
            return 'gzip', gzip.decompress(data)
        except:
            pass

    # 3. В самую последнюю очередь ZLIB или кастомный метод
    if iz_zlib(data):
        try:
            return 'zlib', zlib.decompress(data)
        except:
            pass

    if is_json(data):
        return 'plain', data

    raise ValueError("Неподдерживаемый формат сжатия")


def decompress_message(message):

    meth, content = __try_decompress(message)

    return meth, content.decode('utf-8-sig', errors='ignore')


def pack_message(message, meth, filename_if_zipfile=None):

    message = message.encode('utf-8')

    if meth == 'plain':
        return message

    if meth == 'zlib':
        return zlib.compress(message)

    if meth == 'gzip':
        return gzip.compress(message)

    if meth == 'zipfile' and filename_if_zipfile:
        return pack_to_zipfile(message, filename_if_zipfile)

    raise Exception(f'wrong method for packing: {meth}, filename: {filename_if_zipfile}')


