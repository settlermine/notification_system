import click
import service
import asyncio

from migrations import migrations


@click.group
def cli() -> None:
    pass

@click.command
def init_db() -> None:
    migrations.init_db()

@click.command
def drop_db() -> None:
    migrations.drop_db()

@click.command
@click.option("--user-id", help="User ID")
@click.option(
    "--destination",
    help="Notification destination. Allowed values: telegram, email, sms. Default: email",
    default="email",
)
@click.option("--content", help="Notification text")
def send_notification(user_id: int, destination: str, content: str):
    click.echo(f"Sending notification to user {user_id} via {destination}")
    click.echo(content)
    asyncio.run(service.send_notification(int(user_id), destination, content))


cli.add_command(init_db, "init-db")
cli.add_command(drop_db, "drop-db")
cli.add_command(send_notification, "send-notification")

if __name__ == "__main__":
    cli()
