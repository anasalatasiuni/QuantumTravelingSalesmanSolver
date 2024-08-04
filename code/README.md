# Getting Started

## Install Python 3

I recommend installing Anaconda and creating a new environment:

```
$ conda create --name dwave python=3.8
```

This will create a new environment named `dwave` and switch to it.
Later on you can switch to this environment by activating it as follows:

```
$ conda activate dwave
```

You can list all environments using:

```
$ conda env list
```

## Create D-Wave account

Create a user account on https://cloud.dwavesys.com/leap/login/?next=/leap/

## Install dwave-ocean-sdk

```
$ pip install dwave-ocean-sdk
```

[Log](https://gist.github.com/siddjain/e9597aa1febe617c375dbeee5319fc8d)

## Run `dwave setup`

```
$ dwave setup
```

This will create a file `dwave.conf` on success. I recommend copying this file to your local project directory. Edit
the file to contain:

```
[prod]
token = please replace with your token as necessary
client = qpu
solver = Advantage_system1.1
endpoint = https://cloud.dwavesys.com/sapi/
```

[Log](https://gist.github.com/siddjain/448bae36695d72a19c176953da543e03)

## Test you are able to access the QPU

```
$ dwave ping -s '{"qpu": true}'
```

[Log](https://gist.github.com/siddjain/fb4c07cbad5d39e50d69e81c2511b1c2)

## List all the solvers available

```
$ dwave solvers
```

[Log](https://gist.github.com/siddjain/b229edd138234f168a212a5583421b9b)