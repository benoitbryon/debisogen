"""PasteScript templates."""
import ConfigParser
import os
import sys

from paste.script.templates import Template, var


# Relative directories.
current_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
package_root_dir = os.path.dirname(current_dir)
template_dir = os.path.join(current_dir, 'templates')
configuration_dir = os.path.join(package_root_dir, 'etc')

# Configuration.
default_configuration_file = os.path.join(configuration_dir, 'defaults.cfg')
assert(os.path.exists(default_configuration_file))


def get_default_configuration(section, cfg=default_configuration_file):
    """Get default values for template vars."""
    Config = ConfigParser.ConfigParser()
    Config.read(cfg)
    options = Config.items(section)
    settings = dict(options)
    return settings


class BaseTemplate(Template):
    """Base template."""
    use_cheetah = True


class DebianPreseedTemplate(BaseTemplate):
    """Template to generate Debian preseed file."""
    name = 'debian_preseed'
    _template_dir = os.path.join(template_dir, name)
    defaults = get_default_configuration(name)
    summary = "Debian preseed file."
    vars = [
        var('make_user', 'Create normal user account', defaults['make_user']),
    ]
    booleans = ['make_user']
