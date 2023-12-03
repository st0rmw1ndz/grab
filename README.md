# grab

simple paste system

this is intended to be run as a standalone program, but module support will be put in mind in the future.

all pastes are saved to `~/.grab` in separate files. you can query this directory for a list of available pastes, or use `grab ls`.

## installation

```
pip install git+https://github.com/st0rmw1ndz/grab
```

## usage

```
usage: grab [-h] {copy,write,rm,ls,edit,rename,view,export,upload} ...

simple paste system

options:
  -h, --help            show this help message and exit

commands:
  {copy,write,rm,ls,edit,rename,view,export,upload}
    copy                copy a paste to the clipboard
    write               write a new paste
    rm                  remove a paste
    ls                  list all available pastes
    edit                open a paste in the default text editor
    rename              rename a paste
    view                view a paste
    export              export a paste
    upload              upload a paste
```

note: you can run `grab -h [command]` for more information about a command (such as arguments or default values)

## examples

**writing a new paste from clipboard**

```
> grab write testpaste
paste 'testpaste' saved (size: 15 bytes)

> grab view testpaste
welcome to grab
```

**uploading a paste**

note: as of now, catbox is the only available uploader. more will be added.

```
> grab upload helloworld
https://files.catbox.moe/[REDACTED].txt
```

**listing available pastes**

```
> grab ls
available pastes:
 - anothertest (size: 259 bytes)
 - toothpaste (size: 15 bytes)
```

**exporting a paste to a file**

```
> grab export epicpaste ~/Documents/nicepaste
paste 'epicpaste' exported to '~/Documents/nicepaste'
```

**renaming a paste**

```
> grab rename hello there
paste 'hello' renamed to 'there'
```